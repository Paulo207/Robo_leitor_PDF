"""
Módulo para extrair texto de PDFs de faturas da Coelba
"""
import re
import pdfplumber
from typing import Dict, Optional
from pathlib import Path


class CoelbaPDFReader:
    """Classe para ler e extrair dados de faturas da Coelba em PDF"""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa o leitor de PDF
        
        Args:
            pdf_path: Caminho para o arquivo PDF
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    
    def extract_text(self) -> str:
        """
        Extrai todo o texto do PDF
        
        Returns:
            String com o texto completo do PDF
        """
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
        
        return text
    
    def extract_invoice_data(self) -> Dict[str, Optional[str]]:
        """
        Extrai dados estruturados da fatura da Coelba
        
        Returns:
            Dicionário com os dados extraídos:
            - cliente: Nome do cliente
            - uc: Unidade consumidora
            - mes_referencia: Mês de referência
            - vencimento: Data de vencimento
            - valor_total: Valor total da fatura
            - consumo_kwh: Consumo em kWh
            - impostos: Valores de impostos
        """
        text = self.extract_text()
        
        data = {
            'arquivo': self.pdf_path.name,
            'cliente': self._extract_cliente(text),
            'uc': self._extract_uc(text),
            'mes_referencia': self._extract_mes_referencia(text),
            'vencimento': self._extract_vencimento(text),
            'valor_total': self._extract_valor_total(text),
            'consumo_kwh': self._extract_consumo(text),
            'impostos': self._extract_impostos(text),
        }
        
        return data
    
    def _extract_cliente(self, text: str) -> Optional[str]:
        """Extrai o nome do cliente"""
        # Padrões comuns para nome de cliente em faturas
        patterns = [
            r'(?:Cliente|CLIENTE|Nome):\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ\s]+)',
            r'(?:Nome do Cliente|NOME DO CLIENTE):\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ\s]+)',
            r'^([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ\s]{3,50})$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                cliente = match.group(1).strip()
                # Validar se não é apenas números ou muito curto
                if len(cliente) > 3 and not cliente.isdigit():
                    return cliente
        
        return None
    
    def _extract_uc(self, text: str) -> Optional[str]:
        """Extrai a Unidade Consumidora (UC)"""
        patterns = [
            r'(?:UC|U\.C\.|Unidade Consumidora|UNIDADE CONSUMIDORA)[\s:]*(\d{8,15})',
            r'(?:Número da Instalação|No\. Instalação)[\s:]*(\d{8,15})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_mes_referencia(self, text: str) -> Optional[str]:
        """Extrai o mês de referência"""
        patterns = [
            r'(?:Referência|Ref\.|Mês de Referência|MÊS DE REFERÊNCIA)[\s:]*(\d{2}/\d{4})',
            r'(?:Período|PERÍODO)[\s:]*(\w+/\d{4})',
            r'(\d{2}/\d{2}/\d{4})\s*a\s*\d{2}/\d{2}/\d{4}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_vencimento(self, text: str) -> Optional[str]:
        """Extrai a data de vencimento"""
        patterns = [
            r'(?:Vencimento|VENCIMENTO|Data de Vencimento)[\s:]*(\d{2}/\d{2}/\d{4})',
            r'(?:Vence em|VENCE EM)[\s:]*(\d{2}/\d{2}/\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_valor_total(self, text: str) -> Optional[str]:
        """Extrai o valor total da fatura"""
        patterns = [
            r'(?:Valor Total|VALOR TOTAL|Total a Pagar|TOTAL A PAGAR)[\s:]*R?\$?\s*([\d.,]+)',
            r'(?:Total|TOTAL)[\s:]*R?\$?\s*([\d.,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                valor = match.group(1).strip()
                # Normalizar formato brasileiro (1.234,56) para formato padrão (1234.56)
                # ou formato com ponto como decimal (150.75)
                if ',' in valor and '.' in valor:
                    # Formato brasileiro: 1.234,56 -> 1234.56
                    valor = valor.replace('.', '').replace(',', '.')
                elif ',' in valor:
                    # Formato com vírgula como decimal: 150,75 -> 150.75
                    valor = valor.replace(',', '.')
                # Se só tem ponto, assume que é decimal: 150.75 -> 150.75
                
                # Validar que é um número válido
                try:
                    float(valor)
                    return valor
                except ValueError:
                    continue
        
        return None
    
    def _extract_consumo(self, text: str) -> Optional[str]:
        """Extrai o consumo em kWh"""
        patterns = [
            r'(?:Consumo|CONSUMO)[\s:]*(\d+)\s*kWh',
            r'(\d+)\s*kWh',
            r'(?:Energia Elétrica|ENERGIA ELÉTRICA)[\s:]*(\d+)\s*kWh',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_impostos(self, text: str) -> Optional[str]:
        """Extrai informações sobre impostos"""
        # Procura por valores de impostos comuns: ICMS, PIS, COFINS
        impostos_encontrados = []
        
        # ICMS
        icms_match = re.search(r'(?:ICMS|Icms)[\s:]*R?\$?\s*([\d.,]+)', text, re.IGNORECASE)
        if icms_match:
            impostos_encontrados.append(f"ICMS: {icms_match.group(1)}")
        
        # PIS
        pis_match = re.search(r'(?:PIS|Pis)[\s:]*R?\$?\s*([\d.,]+)', text, re.IGNORECASE)
        if pis_match:
            impostos_encontrados.append(f"PIS: {pis_match.group(1)}")
        
        # COFINS
        cofins_match = re.search(r'(?:COFINS|Cofins)[\s:]*R?\$?\s*([\d.,]+)', text, re.IGNORECASE)
        if cofins_match:
            impostos_encontrados.append(f"COFINS: {cofins_match.group(1)}")
        
        return "; ".join(impostos_encontrados) if impostos_encontrados else None
