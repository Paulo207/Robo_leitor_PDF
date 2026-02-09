"""
Script principal do Robô Leitor de PDFs da Coelba
"""
import os
import sys
from pathlib import Path
from typing import List
import argparse

from pdf_reader import CoelbaPDFReader
from excel_exporter import ExcelExporter


class CoelbaInvoiceProcessor:
    """Processador principal de faturas da Coelba"""
    
    def __init__(self, input_folder: str = "input_pdfs", output_file: str = "output/faturas_coelba.xlsx"):
        """
        Inicializa o processador
        
        Args:
            input_folder: Pasta contendo os PDFs das faturas
            output_file: Arquivo Excel de saída
        """
        self.input_folder = Path(input_folder)
        self.output_file = output_file
        self.exporter = ExcelExporter(output_file)
        
        # Criar pasta de entrada se não existir
        self.input_folder.mkdir(parents=True, exist_ok=True)
    
    def find_pdf_files(self) -> List[Path]:
        """
        Encontra todos os arquivos PDF na pasta de entrada
        
        Returns:
            Lista de caminhos para arquivos PDF
        """
        pdf_files = list(self.input_folder.glob("*.pdf"))
        pdf_files.extend(self.input_folder.glob("*.PDF"))
        return sorted(pdf_files)
    
    def process_single_pdf(self, pdf_path: Path) -> dict:
        """
        Processa um único arquivo PDF
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Dicionário com dados extraídos
        """
        print(f"📄 Processando: {pdf_path.name}")
        
        try:
            reader = CoelbaPDFReader(str(pdf_path))
            data = reader.extract_invoice_data()
            print(f"✓ Dados extraídos com sucesso")
            return data
        except Exception as e:
            print(f"✗ Erro ao processar {pdf_path.name}: {str(e)}")
            return {
                'arquivo': pdf_path.name,
                'erro': str(e)
            }
    
    def process_all_pdfs(self) -> List[dict]:
        """
        Processa todos os PDFs na pasta de entrada
        
        Returns:
            Lista de dicionários com dados extraídos
        """
        pdf_files = self.find_pdf_files()
        
        if not pdf_files:
            print(f"⚠️  Nenhum arquivo PDF encontrado em '{self.input_folder}'")
            return []
        
        print(f"\n🤖 Robô Leitor de PDFs da Coelba")
        print(f"📁 Pasta de entrada: {self.input_folder}")
        print(f"📊 Arquivo de saída: {self.output_file}")
        print(f"📄 Arquivos encontrados: {len(pdf_files)}\n")
        
        all_data = []
        for pdf_path in pdf_files:
            data = self.process_single_pdf(pdf_path)
            all_data.append(data)
        
        return all_data
    
    def export_results(self, data_list: List[dict]) -> str:
        """
        Exporta os resultados para Excel
        
        Args:
            data_list: Lista de dados extraídos
            
        Returns:
            Caminho do arquivo gerado
        """
        if not data_list:
            print("⚠️  Nenhum dado para exportar")
            return None
        
        try:
            output_path = self.exporter.export_to_excel(data_list)
            print(f"\n✓ Planilha gerada com sucesso: {output_path}")
            print(f"📊 Total de faturas processadas: {len(data_list)}")
            return output_path
        except Exception as e:
            print(f"\n✗ Erro ao gerar planilha: {str(e)}")
            return None
    
    def run(self) -> bool:
        """
        Executa o processamento completo
        
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            # Processar todos os PDFs
            data_list = self.process_all_pdfs()
            
            if not data_list:
                return False
            
            # Exportar para Excel
            output_path = self.export_results(data_list)
            
            return output_path is not None
        except Exception as e:
            print(f"\n✗ Erro durante execução: {str(e)}")
            return False


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Robô para leitura automática de faturas da Coelba em PDF'
    )
    parser.add_argument(
        '-i', '--input',
        default='input_pdfs',
        help='Pasta contendo os PDFs das faturas (padrão: input_pdfs)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output/faturas_coelba.xlsx',
        help='Arquivo Excel de saída (padrão: output/faturas_coelba.xlsx)'
    )
    
    args = parser.parse_args()
    
    # Criar e executar o processador
    processor = CoelbaInvoiceProcessor(
        input_folder=args.input,
        output_file=args.output
    )
    
    success = processor.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
