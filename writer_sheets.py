"""
Módulo para escrita de dados em Google Sheets
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Tentar importar gspread
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_DISPONIVEL = True
except ImportError:
    GSPREAD_DISPONIVEL = False
    logger.warning("gspread não instalado. Integração com Google Sheets não disponível.")

load_dotenv()


class WriterSheets:
    """Classe para escrever dados extraídos em Google Sheets"""
    
    def __init__(self, sheet_id: Optional[str] = None, aba: str = "Faturas"):
        self.sheet_id = sheet_id or os.getenv('GOOGLE_SHEET_ID')
        self.aba = aba or os.getenv('GOOGLE_SHEET_ABA', 'Faturas')
        self.cliente = None
        self.planilha = None
        self.worksheet = None
        
        self.colunas = [
            'Cliente', 'UC', 'Mês Referência', 'Data Vencimento',
            'Valor Total', 'Consumo kWh', 'ICMS', 'PIS', 'COFINS', 'CIP',
            'Data Processamento', 'Arquivo PDF'
        ]
        
        if GSPREAD_DISPONIVEL:
            self._autenticar()
    
    def _autenticar(self):
        """Autentica com Google Sheets API"""
        try:
            # Definir escopos necessários
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Autenticar usando arquivo de credenciais
            creds_file = 'credentials.json'
            if not os.path.exists(creds_file):
                logger.warning(f"Arquivo {creds_file} não encontrado. Google Sheets não disponível.")
                return
            
            creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
            self.cliente = gspread.authorize(creds)
            
            # Abrir planilha
            if self.sheet_id:
                self.planilha = self.cliente.open_by_key(self.sheet_id)
                
                # Tentar obter aba ou criar
                try:
                    self.worksheet = self.planilha.worksheet(self.aba)
                except gspread.exceptions.WorksheetNotFound:
                    logger.info(f"Aba '{self.aba}' não encontrada. Criando...")
                    self.worksheet = self.planilha.add_worksheet(
                        title=self.aba, rows=1000, cols=len(self.colunas)
                    )
                    self._criar_cabecalho()
                
                logger.info("Autenticação Google Sheets realizada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao autenticar Google Sheets: {str(e)}")
    
    def _criar_cabecalho(self):
        """Cria cabeçalho na primeira linha"""
        try:
            if self.worksheet:
                self.worksheet.update('A1', [self.colunas])
                
                # Formatar cabeçalho (negrito, cor de fundo)
                self.worksheet.format('A1:L1', {
                    "backgroundColor": {"red": 0.21, "green": 0.38, "blue": 0.57},
                    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                    "horizontalAlignment": "CENTER"
                })
                
                logger.info("Cabeçalho criado no Google Sheets")
                
        except Exception as e:
            logger.error(f"Erro ao criar cabeçalho: {str(e)}")
    
    def adicionar_fatura(self, dados: Dict, arquivo_pdf: str = "") -> bool:
        """
        Adiciona uma nova linha com dados da fatura
        
        Args:
            dados: Dicionário com campos extraídos
            arquivo_pdf: Nome do arquivo PDF processado
            
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.disponivel():
            logger.error("Google Sheets não disponível")
            return False
        
        try:
            # Preparar linha de dados
            linha = [
                dados.get('cliente', ''),
                dados.get('uc', ''),
                dados.get('mes_referencia', ''),
                dados.get('data_vencimento', ''),
                dados.get('valor_total', ''),
                dados.get('consumo_kwh', ''),
                dados.get('impostos', {}).get('icms', ''),
                dados.get('impostos', {}).get('pis', ''),
                dados.get('impostos', {}).get('cofins', ''),
                dados.get('impostos', {}).get('cip', ''),
                datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                arquivo_pdf
            ]
            
            # Adicionar linha
            self.worksheet.append_row(linha)
            logger.info(f"Fatura adicionada ao Google Sheets: UC {dados.get('uc', 'N/A')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar fatura ao Google Sheets: {str(e)}")
            return False
    
    def adicionar_multiplas_faturas(self, lista_dados: List[Dict]) -> int:
        """
        Adiciona múltiplas faturas de uma vez (mais eficiente)
        
        Args:
            lista_dados: Lista de dicionários com dados das faturas
            
        Returns:
            Número de faturas adicionadas com sucesso
        """
        if not self.disponivel():
            return 0
        
        try:
            linhas = []
            for dados in lista_dados:
                linha = [
                    dados.get('cliente', ''),
                    dados.get('uc', ''),
                    dados.get('mes_referencia', ''),
                    dados.get('data_vencimento', ''),
                    dados.get('valor_total', ''),
                    dados.get('consumo_kwh', ''),
                    dados.get('impostos', {}).get('icms', ''),
                    dados.get('impostos', {}).get('pis', ''),
                    dados.get('impostos', {}).get('cofins', ''),
                    dados.get('impostos', {}).get('cip', ''),
                    datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    dados.get('arquivo_pdf', '')
                ]
                linhas.append(linha)
            
            # Adicionar todas de uma vez
            self.worksheet.append_rows(linhas)
            logger.info(f"{len(linhas)} faturas adicionadas ao Google Sheets")
            
            return len(linhas)
            
        except Exception as e:
            logger.error(f"Erro ao adicionar múltiplas faturas: {str(e)}")
            return 0
    
    def verificar_duplicata(self, uc: str, mes_referencia: str) -> bool:
        """
        Verifica se já existe fatura para esta UC e mês
        
        Args:
            uc: Número da unidade consumidora
            mes_referencia: Mês de referência
            
        Returns:
            True se já existe, False caso contrário
        """
        if not self.disponivel():
            return False
        
        try:
            # Obter todos os valores
            valores = self.worksheet.get_all_values()
            
            # Pular cabeçalho
            for linha in valores[1:]:
                if len(linha) >= 3:
                    uc_linha = linha[1]  # Coluna UC
                    mes_linha = linha[2]  # Coluna Mês Referência
                    
                    if str(uc_linha) == str(uc) and str(mes_linha) == str(mes_referencia):
                        logger.warning(f"Duplicata encontrada no Sheets: UC {uc}, Mês {mes_referencia}")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao verificar duplicata: {str(e)}")
            return False
    
    def disponivel(self) -> bool:
        """Verifica se Google Sheets está disponível e configurado"""
        return GSPREAD_DISPONIVEL and self.worksheet is not None
    
    def obter_estatisticas(self) -> Dict:
        """
        Obtém estatísticas das faturas processadas
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.disponivel():
            return {}
        
        try:
            valores = self.worksheet.get_all_values()
            
            # Remover cabeçalho
            dados = valores[1:]
            
            stats = {
                'total_faturas': len(dados),
                'clientes_unicos': len(set(linha[0] for linha in dados if len(linha) > 0)),
                'ucs_unicas': len(set(linha[1] for linha in dados if len(linha) > 1))
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {}
