"""
Script de exemplo para demonstrar o uso do Robô Leitor de PDFs
"""
from pdf_reader import CoelbaPDFReader
from excel_exporter import ExcelExporter
from pathlib import Path


def exemplo_simples():
    """Exemplo simples de uso básico"""
    print("=" * 60)
    print("EXEMPLO 1: Processando um único PDF")
    print("=" * 60)
    
    # Caminho para um PDF de exemplo
    pdf_path = "input_pdfs/fatura_exemplo.pdf"
    
    # Verificar se o arquivo existe
    if not Path(pdf_path).exists():
        print(f"⚠️  Arquivo não encontrado: {pdf_path}")
        print("   Coloque um PDF de fatura da Coelba em 'input_pdfs/'")
        return
    
    # Criar leitor e extrair dados
    reader = CoelbaPDFReader(pdf_path)
    dados = reader.extract_invoice_data()
    
    # Exibir dados extraídos
    print("\n📊 Dados Extraídos:")
    for chave, valor in dados.items():
        print(f"   {chave:20s}: {valor}")
    
    # Exportar para Excel
    exporter = ExcelExporter("output/exemplo_unico.xlsx")
    output_path = exporter.export_to_excel([dados])
    print(f"\n✓ Planilha gerada: {output_path}")


def exemplo_multiplos_pdfs():
    """Exemplo de processamento de múltiplos PDFs"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Processando múltiplos PDFs")
    print("=" * 60)
    
    input_folder = Path("input_pdfs")
    pdf_files = list(input_folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  Nenhum PDF encontrado em '{input_folder}'")
        return
    
    print(f"\n📁 Encontrados {len(pdf_files)} arquivos PDF")
    
    # Processar cada PDF
    todos_dados = []
    for pdf_path in pdf_files:
        print(f"\n📄 Processando: {pdf_path.name}")
        try:
            reader = CoelbaPDFReader(str(pdf_path))
            dados = reader.extract_invoice_data()
            todos_dados.append(dados)
            print("   ✓ Sucesso")
        except Exception as e:
            print(f"   ✗ Erro: {str(e)}")
    
    # Exportar todos para Excel
    if todos_dados:
        exporter = ExcelExporter("output/exemplo_multiplos.xlsx")
        output_path = exporter.export_to_excel(todos_dados)
        print(f"\n✓ Planilha gerada: {output_path}")
        print(f"📊 Total de faturas: {len(todos_dados)}")


def exemplo_apenas_texto():
    """Exemplo de extração apenas do texto do PDF"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Extraindo apenas o texto do PDF")
    print("=" * 60)
    
    pdf_path = "input_pdfs/fatura_exemplo.pdf"
    
    if not Path(pdf_path).exists():
        print(f"⚠️  Arquivo não encontrado: {pdf_path}")
        return
    
    reader = CoelbaPDFReader(pdf_path)
    texto = reader.extract_text()
    
    print("\n📝 Texto extraído (primeiros 500 caracteres):")
    print("-" * 60)
    print(texto[:500])
    print("-" * 60)


if __name__ == "__main__":
    print("\n🤖 EXEMPLOS DE USO DO ROBÔ LEITOR DE PDFs DA COELBA\n")
    
    # Criar pastas necessárias
    Path("input_pdfs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    # Executar exemplos
    try:
        exemplo_simples()
        exemplo_multiplos_pdfs()
        exemplo_apenas_texto()
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Para usar o robô completo, execute: python main.py")
    print("=" * 60)
