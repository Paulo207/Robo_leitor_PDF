"""
Módulo de leitura de PDFs com suporte a OCR
Suporta PDFs com texto nativo e PDFs escaneados (via Tesseract OCR)
"""

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class LeitorPDF:
    """Classe para leitura de PDFs com fallback para OCR"""
    
    def __init__(self, usar_ocr_fallback: bool = True):
        self.usar_ocr_fallback = usar_ocr_fallback
    
    def extrair_texto(self, caminho_pdf: str) -> Optional[str]:
        """
        Extrai texto de um PDF, usando OCR se necessário
        
        Args:
            caminho_pdf: Caminho para o arquivo PDF
            
        Returns:
            Texto extraído ou None em caso de erro
        """
        try:
            # Tentar extrair texto nativo primeiro
            texto = self._extrair_texto_nativo(caminho_pdf)
            
            # Verificar se texto foi extraído com sucesso
            if texto and len(texto.strip()) > 100:
                logger.info(f"Texto extraído com sucesso usando pdfplumber: {caminho_pdf}")
                return texto
            
            # Se texto nativo falhar e OCR estiver habilitado
            if self.usar_ocr_fallback:
                logger.info(f"Texto nativo insuficiente, tentando OCR: {caminho_pdf}")
                texto = self._extrair_texto_ocr(caminho_pdf)
                if texto:
                    logger.info(f"Texto extraído com sucesso usando OCR: {caminho_pdf}")
                    return texto
            
            logger.warning(f"Não foi possível extrair texto suficiente: {caminho_pdf}")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF {caminho_pdf}: {str(e)}")
            return None
    
    def _extrair_texto_nativo(self, caminho_pdf: str) -> Optional[str]:
        """Extrai texto nativo do PDF usando pdfplumber"""
        try:
            texto_completo = []
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(texto)
            
            return "\n".join(texto_completo) if texto_completo else None
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto nativo: {str(e)}")
            return None
    
    def _extrair_texto_ocr(self, caminho_pdf: str) -> Optional[str]:
        """Extrai texto usando OCR (Tesseract) para PDFs escaneados"""
        try:
            # Converter PDF para imagens
            imagens = convert_from_path(caminho_pdf)
            
            texto_completo = []
            for i, imagem in enumerate(imagens):
                # Aplicar OCR em cada página
                texto = pytesseract.image_to_string(imagem, lang='por')
                if texto:
                    texto_completo.append(texto)
                logger.debug(f"OCR aplicado na página {i+1}/{len(imagens)}")
            
            return "\n".join(texto_completo) if texto_completo else None
            
        except Exception as e:
            logger.error(f"Erro ao aplicar OCR: {str(e)}")
            return None
    
    def verificar_pdf_valido(self, caminho_pdf: str) -> bool:
        """
        Verifica se o arquivo é um PDF válido
        
        Args:
            caminho_pdf: Caminho para o arquivo PDF
            
        Returns:
            True se o PDF é válido, False caso contrário
        """
        try:
            caminho = Path(caminho_pdf)
            
            # Verificar se arquivo existe
            if not caminho.exists():
                logger.error(f"Arquivo não encontrado: {caminho_pdf}")
                return False
            
            # Verificar extensão
            if caminho.suffix.lower() != '.pdf':
                logger.error(f"Arquivo não é PDF: {caminho_pdf}")
                return False
            
            # Tentar abrir o PDF
            with pdfplumber.open(caminho_pdf) as pdf:
                if len(pdf.pages) == 0:
                    logger.error(f"PDF sem páginas: {caminho_pdf}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao validar PDF {caminho_pdf}: {str(e)}")
            return False
    
    def obter_info_pdf(self, caminho_pdf: str) -> Dict:
        """
        Obtém informações sobre o PDF
        
        Args:
            caminho_pdf: Caminho para o arquivo PDF
            
        Returns:
            Dicionário com informações do PDF
        """
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                return {
                    'num_paginas': len(pdf.pages),
                    'metadata': pdf.metadata,
                    'caminho': caminho_pdf
                }
        except Exception as e:
            logger.error(f"Erro ao obter info do PDF: {str(e)}")
            return {}
