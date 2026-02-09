"""
Módulo de monitoramento de pasta para processamento automático
"""

import time
import logging
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import os

logger = logging.getLogger(__name__)


class ManipuladorPDF(FileSystemEventHandler):
    """Handler para eventos de criação de arquivos PDF"""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.processando = set()
    
    def on_created(self, event: FileCreatedEvent):
        """Chamado quando um arquivo é criado"""
        if event.is_directory:
            return
        
        caminho = event.src_path
        
        # Verificar se é PDF
        if not caminho.lower().endswith('.pdf'):
            return
        
        # Evitar processar o mesmo arquivo múltiplas vezes
        if caminho in self.processando:
            return
        
        # Aguardar o arquivo ser completamente copiado
        time.sleep(2)
        
        # Verificar se arquivo ainda existe (pode ter sido movido)
        if not os.path.exists(caminho):
            return
        
        logger.info(f"Novo PDF detectado: {caminho}")
        self.processando.add(caminho)
        
        try:
            # Chamar callback de processamento
            self.callback(caminho)
        finally:
            self.processando.discard(caminho)


class MonitorPasta:
    """Classe para monitorar pasta e processar PDFs automaticamente"""
    
    def __init__(self, pasta_entrada: str, callback_processamento: Callable[[str], None]):
        self.pasta_entrada = Path(pasta_entrada)
        self.callback_processamento = callback_processamento
        self.observer = None
        self.rodando = False
        
        # Criar pasta se não existir
        self.pasta_entrada.mkdir(parents=True, exist_ok=True)
    
    def iniciar(self):
        """Inicia o monitoramento da pasta"""
        try:
            # Criar observer
            self.observer = Observer()
            handler = ManipuladorPDF(self.callback_processamento)
            
            # Agendar monitoramento
            self.observer.schedule(handler, str(self.pasta_entrada), recursive=False)
            
            # Iniciar
            self.observer.start()
            self.rodando = True
            
            logger.info(f"Monitoramento iniciado: {self.pasta_entrada}")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar monitoramento: {str(e)}")
            self.rodando = False
    
    def parar(self):
        """Para o monitoramento"""
        if self.observer and self.rodando:
            self.observer.stop()
            self.observer.join()
            self.rodando = False
            logger.info("Monitoramento parado")
    
    def processar_existentes(self):
        """Processa PDFs que já existem na pasta"""
        try:
            pdfs = list(self.pasta_entrada.glob('*.pdf'))
            
            if not pdfs:
                logger.info("Nenhum PDF encontrado para processar")
                return
            
            logger.info(f"Encontrados {len(pdfs)} PDFs para processar")
            
            for pdf in pdfs:
                try:
                    logger.info(f"Processando arquivo existente: {pdf.name}")
                    self.callback_processamento(str(pdf))
                except Exception as e:
                    logger.error(f"Erro ao processar {pdf.name}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivos existentes: {str(e)}")
    
    def aguardar(self):
        """Mantém o monitoramento rodando indefinidamente"""
        if not self.rodando:
            logger.error("Monitoramento não está rodando")
            return
        
        try:
            while self.rodando:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário")
            self.parar()
    
    def contar_pdfs_pendentes(self) -> int:
        """Conta quantos PDFs estão na pasta de entrada"""
        try:
            return len(list(self.pasta_entrada.glob('*.pdf')))
        except:
            return 0
