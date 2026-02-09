"""
Módulo principal de processamento de faturas
Orquestra todo o fluxo de extração e armazenamento
"""

import logging
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from leitor_pdf import LeitorPDF
from extrator_campos import ExtratorCampos
from extrator_ia import ExtratorIA
from writer_excel import WriterExcel
from writer_sheets import WriterSheets

load_dotenv()
logger = logging.getLogger(__name__)


class ProcessadorFatura:
    """Classe principal para processar faturas"""
    
    def __init__(self, config_path: str = "config_campos.json"):
        # Carregar configurações
        self.config = self._carregar_config(config_path)
        
        # Inicializar componentes
        self.leitor_pdf = LeitorPDF(
            usar_ocr_fallback=os.getenv('USAR_OCR_FALLBACK', 'true').lower() == 'true'
        )
        self.extrator_campos = ExtratorCampos(config_path)
        self.extrator_ia = ExtratorIA()
        
        # Configurar pastas
        self.pasta_entrada = Path(os.getenv('PASTA_ENTRADA', 'entrada_pdfs'))
        self.pasta_processados = Path(os.getenv('PASTA_PROCESSADOS', 'processados'))
        self.pasta_erros = Path(os.getenv('PASTA_ERROS', 'erros'))
        self.pasta_logs = Path(os.getenv('PASTA_LOGS', 'logs'))
        
        # Criar pastas
        for pasta in [self.pasta_entrada, self.pasta_processados, self.pasta_erros, self.pasta_logs]:
            pasta.mkdir(parents=True, exist_ok=True)
        
        # Inicializar writers
        self.usar_excel = os.getenv('USAR_EXCEL', 'true').lower() == 'true'
        self.usar_sheets = os.getenv('USAR_GOOGLE_SHEETS', 'false').lower() == 'true'
        
        self.writer_excel = WriterExcel(os.getenv('ARQUIVO_EXCEL', 'faturas_coelba.xlsx'))
        self.writer_sheets = WriterSheets() if self.usar_sheets else None
        
        # Estatísticas
        self.stats = {
            'total': 0,
            'sucesso': 0,
            'erro': 0,
            'duplicatas': 0
        }
    
    def _carregar_config(self, config_path: str) -> Dict:
        """Carrega configuração"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar config: {str(e)}")
            return {}
    
    def processar_pdf(self, caminho_pdf: str) -> Tuple[bool, Optional[Dict]]:
        """
        Processa um único PDF
        
        Args:
            caminho_pdf: Caminho para o arquivo PDF
            
        Returns:
            Tupla (sucesso, dados_extraidos)
        """
        self.stats['total'] += 1
        nome_arquivo = Path(caminho_pdf).name
        
        logger.info(f"Iniciando processamento: {nome_arquivo}")
        
        try:
            # 1. Validar PDF
            if not self.leitor_pdf.verificar_pdf_valido(caminho_pdf):
                logger.error(f"PDF inválido: {nome_arquivo}")
                self._mover_para_erros(caminho_pdf, "pdf_invalido")
                self.stats['erro'] += 1
                return False, None
            
            # 2. Extrair texto
            texto = self.leitor_pdf.extrair_texto(caminho_pdf)
            if not texto:
                logger.error(f"Não foi possível extrair texto: {nome_arquivo}")
                self._mover_para_erros(caminho_pdf, "extracao_texto_falhou")
                self.stats['erro'] += 1
                return False, None
            
            # 3. Extrair campos com regex
            dados = self.extrator_campos.extrair_campos(texto)
            
            # 4. Usar IA como fallback se necessário
            usar_ia = os.getenv('USAR_IA_FALLBACK', 'true').lower() == 'true'
            if usar_ia and self.extrator_ia.disponivel():
                if not self.extrator_campos.validar_extracao(dados):
                    logger.info("Extração incompleta, usando IA como fallback")
                    dados = self.extrator_ia.melhorar_extracao(dados, texto)
            
            # 5. Validar extração
            if not self.extrator_campos.validar_extracao(dados):
                logger.error(f"Extração incompleta: {nome_arquivo}")
                self._mover_para_erros(caminho_pdf, "extracao_incompleta")
                self._salvar_dados_parciais(dados, nome_arquivo)
                self.stats['erro'] += 1
                return False, dados
            
            # 6. Verificar duplicatas
            uc = dados.get('uc', '')
            mes_ref = dados.get('mes_referencia', '')
            
            if self.usar_excel and self.writer_excel.verificar_duplicata(uc, mes_ref):
                logger.warning(f"Duplicata detectada: {nome_arquivo}")
                self._mover_para_processados(caminho_pdf, dados, sufixo="_duplicata")
                self.stats['duplicatas'] += 1
                return False, dados
            
            # 7. Salvar nos sistemas de saída
            dados['arquivo_pdf'] = nome_arquivo
            
            if self.usar_excel:
                if not self.writer_excel.adicionar_fatura(dados, nome_arquivo):
                    logger.error(f"Erro ao salvar no Excel: {nome_arquivo}")
                    self._mover_para_erros(caminho_pdf, "erro_excel")
                    self.stats['erro'] += 1
                    return False, dados
            
            if self.usar_sheets and self.writer_sheets and self.writer_sheets.disponivel():
                if not self.writer_sheets.adicionar_fatura(dados, nome_arquivo):
                    logger.warning(f"Erro ao salvar no Sheets: {nome_arquivo}")
            
            # 8. Mover para processados
            self._mover_para_processados(caminho_pdf, dados)
            
            # 9. Log de sucesso
            self._log_processamento(nome_arquivo, dados, True)
            
            self.stats['sucesso'] += 1
            logger.info(f"Processamento concluído com sucesso: {nome_arquivo}")
            
            return True, dados
            
        except Exception as e:
            logger.error(f"Erro ao processar {nome_arquivo}: {str(e)}", exc_info=True)
            self._mover_para_erros(caminho_pdf, "erro_processamento")
            self.stats['erro'] += 1
            return False, None
    
    def _mover_para_processados(self, caminho_pdf: str, dados: Dict, sufixo: str = ""):
        """Move PDF para pasta de processados com nome organizado"""
        try:
            caminho = Path(caminho_pdf)
            
            # Gerar novo nome se configurado
            renomear = os.getenv('RENOMEAR_ARQUIVOS', 'true').lower() == 'true'
            
            if renomear and dados:
                uc = dados.get('uc', 'sem_uc')
                mes_ref = dados.get('mes_referencia', '')
                mes, ano = self.extrator_campos.extrair_mes_ano(mes_ref)
                
                if mes and ano:
                    novo_nome = f"{uc}_{mes}_{ano}{sufixo}.pdf"
                else:
                    novo_nome = f"{uc}_{datetime.now().strftime('%Y%m%d')}{sufixo}.pdf"
            else:
                novo_nome = caminho.name
            
            destino = self.pasta_processados / novo_nome
            
            # Evitar sobrescrever
            contador = 1
            while destino.exists():
                nome_base = destino.stem
                destino = self.pasta_processados / f"{nome_base}_{contador}.pdf"
                contador += 1
            
            shutil.move(str(caminho), str(destino))
            logger.info(f"Movido para processados: {novo_nome}")
            
        except Exception as e:
            logger.error(f"Erro ao mover para processados: {str(e)}")
    
    def _mover_para_erros(self, caminho_pdf: str, motivo: str = "erro"):
        """Move PDF para pasta de erros"""
        try:
            caminho = Path(caminho_pdf)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            novo_nome = f"{caminho.stem}_{motivo}_{timestamp}.pdf"
            destino = self.pasta_erros / novo_nome
            
            shutil.move(str(caminho), str(destino))
            logger.info(f"Movido para erros: {novo_nome}")
            
        except Exception as e:
            logger.error(f"Erro ao mover para pasta de erros: {str(e)}")
    
    def _salvar_dados_parciais(self, dados: Dict, nome_arquivo: str):
        """Salva dados parcialmente extraídos em JSON"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_json = f"{Path(nome_arquivo).stem}_{timestamp}.json"
            caminho_json = self.pasta_logs / nome_json
            
            with open(caminho_json, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dados parciais salvos: {nome_json}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar dados parciais: {str(e)}")
    
    def _log_processamento(self, nome_arquivo: str, dados: Dict, sucesso: bool):
        """Registra log de processamento"""
        try:
            log_file = self.pasta_logs / "processamento.log"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                status = "SUCESSO" if sucesso else "ERRO"
                uc = dados.get('uc', 'N/A') if dados else 'N/A'
                
                f.write(f"{timestamp} | {status} | {nome_arquivo} | UC: {uc}\n")
            
        except Exception as e:
            logger.error(f"Erro ao registrar log: {str(e)}")
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas de processamento"""
        return self.stats.copy()
    
    def resetar_estatisticas(self):
        """Reseta contadores de estatísticas"""
        self.stats = {
            'total': 0,
            'sucesso': 0,
            'erro': 0,
            'duplicatas': 0
        }
