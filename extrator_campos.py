"""
Módulo de extração de campos usando Regex e busca por proximidade
"""

import re
import json
import logging
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class ExtratorCampos:
    """Classe para extração de campos de faturas usando regex"""
    
    def __init__(self, config_path: str = "config_campos.json"):
        self.config = self._carregar_config(config_path)
        self.campo_config = self.config.get('campo_configuracoes', {})
    
    def _carregar_config(self, config_path: str) -> Dict:
        """Carrega configuração de campos do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            return {}
    
    def extrair_campos(self, texto: str) -> Dict:
        """
        Extrai todos os campos configurados do texto
        
        Args:
            texto: Texto extraído do PDF
            
        Returns:
            Dicionário com campos extraídos
        """
        resultado = {
            "cliente": self._extrair_campo(texto, "cliente"),
            "uc": self._extrair_campo(texto, "uc"),
            "mes_referencia": self._extrair_campo(texto, "mes_referencia"),
            "data_vencimento": self._extrair_campo(texto, "data_vencimento"),
            "valor_total": self._extrair_campo(texto, "valor_total"),
            "consumo_kwh": self._extrair_campo(texto, "consumo_kwh"),
            "impostos": {
                "icms": self._extrair_campo(texto, "icms"),
                "pis": self._extrair_campo(texto, "pis"),
                "cofins": self._extrair_campo(texto, "cofins"),
                "cip": self._extrair_campo(texto, "cip")
            }
        }
        
        # Limpar valores monetários
        resultado = self._limpar_valores(resultado)
        
        logger.info(f"Campos extraídos: {self._contar_campos_extraidos(resultado)} de 10")
        return resultado
    
    def _extrair_campo(self, texto: str, nome_campo: str) -> Optional[str]:
        """
        Extrai um campo específico do texto
        
        Args:
            texto: Texto do PDF
            nome_campo: Nome do campo a extrair
            
        Returns:
            Valor extraído ou None
        """
        config = self.campo_config.get(nome_campo, {})
        labels = config.get('labels', [])
        pattern = config.get('pattern', '')
        
        # Tentar cada label configurado
        for label in labels:
            # Método 1: Busca por proximidade (label + valor)
            valor = self._buscar_por_proximidade(texto, label, pattern)
            if valor:
                logger.debug(f"Campo '{nome_campo}' encontrado via proximidade: {valor}")
                return valor
            
            # Método 2: Busca por padrão regex geral
            valor = self._buscar_por_pattern(texto, label, pattern)
            if valor:
                logger.debug(f"Campo '{nome_campo}' encontrado via pattern: {valor}")
                return valor
        
        logger.warning(f"Campo '{nome_campo}' não encontrado")
        return None
    
    def _buscar_por_proximidade(self, texto: str, label: str, pattern: str) -> Optional[str]:
        """Busca valor próximo ao label usando regex"""
        try:
            # Criar regex para buscar label seguido de valor
            # Permitir espaços, dois pontos, etc. entre label e valor
            regex_proximidade = rf'{re.escape(label)}\s*:?\s*({pattern})'
            
            match = re.search(regex_proximidade, texto, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
            
            # Tentar buscar em linha próxima (até 100 caracteres depois)
            regex_proxima_linha = rf'{re.escape(label)}[\s\S]{{0,100}}?({pattern})'
            match = re.search(regex_proxima_linha, texto, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na busca por proximidade: {str(e)}")
            return None
    
    def _buscar_por_pattern(self, texto: str, label: str, pattern: str) -> Optional[str]:
        """Busca valor usando apenas o padrão, em contexto do label"""
        try:
            # Encontrar posição do label
            pos_label = texto.lower().find(label.lower())
            if pos_label == -1:
                return None
            
            # Buscar padrão nos próximos 200 caracteres após o label
            texto_contexto = texto[pos_label:pos_label + 200]
            match = re.search(pattern, texto_contexto, re.IGNORECASE)
            
            if match:
                return match.group(0).strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na busca por pattern: {str(e)}")
            return None
    
    def _limpar_valores(self, resultado: Dict) -> Dict:
        """Limpa e normaliza valores extraídos"""
        # Limpar valor total
        if resultado.get('valor_total'):
            resultado['valor_total'] = self._limpar_valor_monetario(resultado['valor_total'])
        
        # Limpar impostos
        for imposto in ['icms', 'pis', 'cofins', 'cip']:
            if resultado['impostos'].get(imposto):
                resultado['impostos'][imposto] = self._limpar_valor_monetario(
                    resultado['impostos'][imposto]
                )
        
        # Limpar consumo
        if resultado.get('consumo_kwh'):
            resultado['consumo_kwh'] = self._limpar_consumo(resultado['consumo_kwh'])
        
        return resultado
    
    def _limpar_valor_monetario(self, valor: str) -> str:
        """Remove símbolos e normaliza valores monetários"""
        # Remover R$, espaços extras
        valor = re.sub(r'R?\$?\s*', '', valor)
        return valor.strip()
    
    def _limpar_consumo(self, valor: str) -> str:
        """Remove unidade kWh e normaliza"""
        valor = re.sub(r'\s*kWh', '', valor, flags=re.IGNORECASE)
        return valor.strip()
    
    def _contar_campos_extraidos(self, resultado: Dict) -> int:
        """Conta quantos campos foram extraídos com sucesso"""
        count = 0
        for key, value in resultado.items():
            if key == 'impostos':
                count += sum(1 for v in value.values() if v)
            elif value:
                count += 1
        return count
    
    def validar_extracao(self, resultado: Dict) -> bool:
        """
        Valida se os campos obrigatórios foram extraídos
        
        Args:
            resultado: Dicionário com campos extraídos
            
        Returns:
            True se validação passar, False caso contrário
        """
        campos_obrigatorios = ['cliente', 'uc', 'data_vencimento', 'valor_total']
        
        for campo in campos_obrigatorios:
            if not resultado.get(campo):
                logger.warning(f"Campo obrigatório '{campo}' não encontrado")
                return False
        
        return True
    
    def extrair_mes_ano(self, mes_referencia: str) -> tuple:
        """
        Extrai mês e ano da referência
        
        Args:
            mes_referencia: String com mês de referência (ex: "01/2024" ou "JAN/2024")
            
        Returns:
            Tupla (mês, ano)
        """
        if not mes_referencia:
            return (None, None)
        
        # Tentar padrão MM/YYYY
        match = re.search(r'(\d{2})/(\d{4})', mes_referencia)
        if match:
            return (match.group(1), match.group(2))
        
        # Tentar padrão MMM/YYYY
        match = re.search(r'([A-Z]{3})/(\d{4})', mes_referencia, re.IGNORECASE)
        if match:
            meses = {
                'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
                'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
                'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
            }
            mes_nome = match.group(1).upper()
            mes_num = meses.get(mes_nome, '01')
            return (mes_num, match.group(2))
        
        return (None, None)
