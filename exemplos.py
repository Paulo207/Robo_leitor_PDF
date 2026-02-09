"""
Script de exemplo demonstrando como usar o sistema RPA COELBA
Este exemplo mostra o fluxo básico sem processar PDFs reais
"""


def exemplo_processamento_basico():
    """Exemplo de processamento básico"""
    print("=" * 60)
    print("EXEMPLO 1: Processamento Básico")
    print("=" * 60)
    
    print("""
# Importar o processador
from processador import ProcessadorFatura

# Criar instância do processador
processador = ProcessadorFatura()

# Processar um único PDF
sucesso, dados = processador.processar_pdf("entrada_pdfs/fatura.pdf")

if sucesso:
    print("PDF processado com sucesso!")
    print(f"Cliente: {dados['cliente']}")
    print(f"UC: {dados['uc']}")
    print(f"Valor: {dados['valor_total']}")
else:
    print("Erro no processamento")
    """)


def exemplo_monitoramento_automatico():
    """Exemplo de monitoramento automático"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Monitoramento Automático")
    print("=" * 60)
    
    print("""
# Importar módulos necessários
from processador import ProcessadorFatura
from monitor_pasta import MonitorPasta

# Criar processador
processador = ProcessadorFatura()

# Criar monitor
monitor = MonitorPasta(
    pasta_entrada="entrada_pdfs",
    callback_processamento=processador.processar_pdf
)

# Processar PDFs existentes
monitor.processar_existentes()

# Iniciar monitoramento contínuo
monitor.iniciar()

# Aguardar (Ctrl+C para parar)
monitor.aguardar()
    """)


def exemplo_processamento_lote():
    """Exemplo de processamento em lote"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Processamento em Lote")
    print("=" * 60)
    
    print("""
from pathlib import Path
from processador import ProcessadorFatura

# Criar processador
processador = ProcessadorFatura()

# Buscar todos os PDFs na pasta
pasta = Path("entrada_pdfs")
pdfs = list(pasta.glob("*.pdf"))

print(f"Encontrados {len(pdfs)} PDFs para processar")

# Processar cada um
for i, pdf in enumerate(pdfs, 1):
    print(f"Processando {i}/{len(pdfs)}: {pdf.name}")
    
    sucesso, dados = processador.processar_pdf(str(pdf))
    
    if sucesso:
        print(f"  ✓ Sucesso: {dados['uc']}")
    else:
        print(f"  ✗ Erro")

# Mostrar estatísticas
stats = processador.obter_estatisticas()
print(f"\\nTotal: {stats['total']}")
print(f"Sucesso: {stats['sucesso']}")
print(f"Erros: {stats['erro']}")
    """)


def exemplo_extracao_customizada():
    """Exemplo de extração customizada"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Extração Customizada")
    print("=" * 60)
    
    print("""
from leitor_pdf import LeitorPDF
from extrator_campos import ExtratorCampos

# Criar extratores
leitor = LeitorPDF(usar_ocr_fallback=True)
extrator = ExtratorCampos("config_campos.json")

# Extrair texto do PDF
texto = leitor.extrair_texto("entrada_pdfs/fatura.pdf")

if texto:
    # Extrair campos
    dados = extrator.extrair_campos(texto)
    
    # Validar
    if extrator.validar_extracao(dados):
        print("Campos extraídos com sucesso!")
        
        # Acessar dados
        print(f"Cliente: {dados['cliente']}")
        print(f"UC: {dados['uc']}")
        print(f"Valor: {dados['valor_total']}")
        print(f"Consumo: {dados['consumo_kwh']} kWh")
        
        # Impostos
        impostos = dados['impostos']
        print(f"ICMS: {impostos['icms']}")
        print(f"PIS: {impostos['pis']}")
        print(f"COFINS: {impostos['cofins']}")
    else:
        print("Extração incompleta")
    """)


def exemplo_excel():
    """Exemplo de uso do Excel"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Salvamento em Excel")
    print("=" * 60)
    
    print("""
from writer_excel import WriterExcel

# Criar writer
writer = WriterExcel("minhas_faturas.xlsx")

# Criar planilha modelo (primeira vez)
writer.criar_planilha_modelo()

# Adicionar fatura
dados = {
    "cliente": "João Silva",
    "uc": "1234567890",
    "mes_referencia": "01/2024",
    "data_vencimento": "15/02/2024",
    "valor_total": "R$ 350,00",
    "consumo_kwh": "250",
    "impostos": {
        "icms": "R$ 50,00",
        "pis": "R$ 10,00",
        "cofins": "R$ 15,00",
        "cip": "R$ 5,00"
    }
}

sucesso = writer.adicionar_fatura(dados, "fatura_jan2024.pdf")

if sucesso:
    print("Fatura adicionada ao Excel!")

# Obter estatísticas
stats = writer.obter_estatisticas()
print(f"Total de faturas: {stats['total_faturas']}")
print(f"Valor total: R$ {stats['valor_total_soma']:.2f}")
    """)


def exemplo_google_sheets():
    """Exemplo de uso do Google Sheets"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Salvamento em Google Sheets")
    print("=" * 60)
    
    print("""
from writer_sheets import WriterSheets

# Criar writer (precisa de credentials.json)
writer = WriterSheets(
    sheet_id="seu_id_da_planilha",
    aba="Faturas"
)

# Verificar se está disponível
if writer.disponivel():
    # Adicionar fatura
    dados = {
        "cliente": "Maria Santos",
        "uc": "9876543210",
        "mes_referencia": "01/2024",
        "data_vencimento": "20/02/2024",
        "valor_total": "R$ 420,00",
        "consumo_kwh": "300",
        "impostos": {
            "icms": "R$ 60,00",
            "pis": "R$ 12,00",
            "cofins": "R$ 18,00",
            "cip": "R$ 6,00"
        }
    }
    
    sucesso = writer.adicionar_fatura(dados, "fatura_jan2024.pdf")
    
    if sucesso:
        print("Fatura adicionada ao Google Sheets!")
else:
    print("Google Sheets não configurado")
    """)


def exemplo_ia_fallback():
    """Exemplo de uso da IA como fallback"""
    print("\n" + "=" * 60)
    print("EXEMPLO 7: IA como Fallback")
    print("=" * 60)
    
    print("""
from extrator_ia import ExtratorIA
from extrator_campos import ExtratorCampos
from leitor_pdf import LeitorPDF

# Criar extratores
leitor = LeitorPDF()
extrator_regex = ExtratorCampos()
extrator_ia = ExtratorIA()  # Requer OPENAI_API_KEY no .env

# Extrair texto
texto = leitor.extrair_texto("entrada_pdfs/fatura_dificil.pdf")

# Tentar regex primeiro
dados = extrator_regex.extrair_campos(texto)

# Se extração incompleta, usar IA
if not extrator_regex.validar_extracao(dados):
    print("Regex incompleto, usando IA...")
    
    if extrator_ia.disponivel():
        # Melhorar extração com IA
        dados = extrator_ia.melhorar_extracao(dados, texto)
        print("IA preencheu campos faltantes!")
    else:
        print("IA não disponível (configure OPENAI_API_KEY)")

print("Resultado final:", dados)
    """)


def mostrar_estrutura_dados():
    """Mostra a estrutura de dados retornada"""
    print("\n" + "=" * 60)
    print("ESTRUTURA DE DADOS")
    print("=" * 60)
    
    print("""
A estrutura de dados retornada pelo sistema:

{
    "cliente": "Nome do Cliente",
    "uc": "1234567890",
    "mes_referencia": "01/2024",
    "data_vencimento": "15/02/2024",
    "valor_total": "R$ 350,00",
    "consumo_kwh": "250",
    "impostos": {
        "icms": "R$ 50,00",
        "pis": "R$ 10,00",
        "cofins": "R$ 15,00",
        "cip": "R$ 5,00"
    },
    "arquivo_pdf": "fatura.pdf"
}
    """)


def main():
    """Função principal"""
    print("\n" + "=" * 70)
    print(" " * 15 + "📚 EXEMPLOS DE USO - RPA COELBA")
    print("=" * 70)
    
    print("""
Este arquivo contém exemplos de código mostrando como usar o sistema.

IMPORTANTE: Para executar estes exemplos, você precisa:
1. Instalar as dependências: pip install -r requirements.txt
2. Configurar o arquivo .env
3. Ter PDFs de faturas COELBA na pasta entrada_pdfs/

Para começar rapidamente:
    python setup.py       # Configuração inicial
    streamlit run app.py  # Interface web
    """)
    
    input("\nPressione ENTER para ver os exemplos...")
    
    # Mostrar exemplos
    exemplo_processamento_basico()
    exemplo_monitoramento_automatico()
    exemplo_processamento_lote()
    exemplo_extracao_customizada()
    exemplo_excel()
    exemplo_google_sheets()
    exemplo_ia_fallback()
    mostrar_estrutura_dados()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "📖 Consulte MANUAL.md para mais detalhes")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
