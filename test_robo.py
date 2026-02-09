"""
Testes básicos para validar os módulos do robô
"""
import unittest
from pathlib import Path
import sys

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent))

from pdf_reader import CoelbaPDFReader
from excel_exporter import ExcelExporter


class TestPDFReader(unittest.TestCase):
    """Testes para o módulo pdf_reader"""
    
    def test_pdf_reader_initialization(self):
        """Testa se o leitor de PDF é inicializado corretamente"""
        # Teste com arquivo inexistente deve lançar exceção
        with self.assertRaises(FileNotFoundError):
            reader = CoelbaPDFReader("arquivo_nao_existe.pdf")
    
    def test_extract_uc_pattern(self):
        """Testa extração de UC com texto de exemplo"""
        # Criar um leitor mock (sem arquivo real)
        text = "Unidade Consumidora: 123456789"
        reader = CoelbaPDFReader.__new__(CoelbaPDFReader)
        uc = reader._extract_uc(text)
        self.assertEqual(uc, "123456789")
    
    def test_extract_valor_pattern(self):
        """Testa extração de valor com texto de exemplo"""
        text = "Valor Total: R$ 150,75"
        reader = CoelbaPDFReader.__new__(CoelbaPDFReader)
        valor = reader._extract_valor_total(text)
        self.assertEqual(valor, "150.75")
    
    def test_extract_consumo_pattern(self):
        """Testa extração de consumo com texto de exemplo"""
        text = "Consumo: 350 kWh"
        reader = CoelbaPDFReader.__new__(CoelbaPDFReader)
        consumo = reader._extract_consumo(text)
        self.assertEqual(consumo, "350")


class TestExcelExporter(unittest.TestCase):
    """Testes para o módulo excel_exporter"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.test_output = Path("test_output.xlsx")
        self.exporter = ExcelExporter(str(self.test_output))
    
    def tearDown(self):
        """Limpeza após cada teste"""
        if self.test_output.exists():
            self.test_output.unlink()
    
    def test_excel_exporter_initialization(self):
        """Testa inicialização do exportador"""
        self.assertIsNotNone(self.exporter)
        self.assertEqual(self.exporter.output_path.name, "test_output.xlsx")
    
    def test_export_to_excel_empty_data(self):
        """Testa exportação com dados vazios"""
        with self.assertRaises(ValueError):
            self.exporter.export_to_excel([])
    
    def test_export_to_excel_single_record(self):
        """Testa exportação de um único registro"""
        data = [{
            'arquivo': 'teste.pdf',
            'cliente': 'João Silva',
            'uc': '123456789',
            'mes_referencia': '12/2023',
            'vencimento': '15/01/2024',
            'valor_total': '150.75',
            'consumo_kwh': '350',
            'impostos': 'ICMS: 30.15'
        }]
        
        output_path = self.exporter.export_to_excel(data)
        self.assertTrue(Path(output_path).exists())
    
    def test_export_to_excel_multiple_records(self):
        """Testa exportação de múltiplos registros"""
        data = [
            {
                'arquivo': 'teste1.pdf',
                'cliente': 'João Silva',
                'valor_total': '150.75',
            },
            {
                'arquivo': 'teste2.pdf',
                'cliente': 'Maria Santos',
                'valor_total': '200.50',
            }
        ]
        
        output_path = self.exporter.export_to_excel(data)
        self.assertTrue(Path(output_path).exists())


def run_tests():
    """Executa todos os testes"""
    print("🧪 Executando testes do Robô Leitor de PDFs\n")
    
    # Criar test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestPDFReader))
    suite.addTests(loader.loadTestsFromTestCase(TestExcelExporter))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar resultado
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
