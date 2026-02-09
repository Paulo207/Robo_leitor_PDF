"""
Script simples para testar o sistema RPA COELBA
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from processador import ProcessadorFatura


def teste_basico():
    """Teste básico do sistema"""
    print("=" * 60)
    print("TESTE DO SISTEMA RPA COELBA")
    print("=" * 60)
    
    # Criar processador
    print("\n1. Inicializando processador...")
    try:
        processador = ProcessadorFatura()
        print("   ✓ Processador inicializado com sucesso")
    except Exception as e:
        print(f"   ✗ Erro ao inicializar: {str(e)}")
        return False
    
    # Verificar pastas
    print("\n2. Verificando estrutura de pastas...")
    pastas = ['entrada_pdfs', 'processados', 'erros', 'logs']
    for pasta in pastas:
        if Path(pasta).exists():
            print(f"   ✓ Pasta '{pasta}' existe")
        else:
            print(f"   ✗ Pasta '{pasta}' não encontrada")
    
    # Verificar arquivos de configuração
    print("\n3. Verificando arquivos de configuração...")
    configs = ['config_campos.json', '.env.example', 'requirements.txt']
    for config in configs:
        if Path(config).exists():
            print(f"   ✓ Arquivo '{config}' existe")
        else:
            print(f"   ✗ Arquivo '{config}' não encontrado")
    
    # Verificar PDFs na pasta de entrada
    print("\n4. Verificando PDFs para processar...")
    pasta_entrada = Path('entrada_pdfs')
    pdfs = list(pasta_entrada.glob('*.pdf'))
    
    if pdfs:
        print(f"   ℹ Encontrados {len(pdfs)} PDF(s):")
        for pdf in pdfs:
            print(f"     - {pdf.name}")
        
        # Perguntar se deseja processar
        resposta = input("\n   Deseja processar estes PDFs? (s/n): ")
        if resposta.lower() == 's':
            print("\n5. Processando PDFs...")
            for i, pdf in enumerate(pdfs, 1):
                print(f"\n   Processando {i}/{len(pdfs)}: {pdf.name}")
                sucesso, dados = processador.processar_pdf(str(pdf))
                
                if sucesso:
                    print(f"   ✓ Sucesso!")
                    if dados:
                        print(f"     Cliente: {dados.get('cliente', 'N/A')}")
                        print(f"     UC: {dados.get('uc', 'N/A')}")
                        print(f"     Valor: {dados.get('valor_total', 'N/A')}")
                else:
                    print(f"   ✗ Erro no processamento")
    else:
        print("   ℹ Nenhum PDF encontrado na pasta de entrada")
        print("   → Coloque arquivos PDF na pasta 'entrada_pdfs' e execute novamente")
    
    # Estatísticas
    print("\n6. Estatísticas do processamento:")
    stats = processador.obter_estatisticas()
    print(f"   Total: {stats['total']}")
    print(f"   Sucesso: {stats['sucesso']}")
    print(f"   Erros: {stats['erro']}")
    print(f"   Duplicatas: {stats['duplicatas']}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)
    
    return True


def teste_modulos():
    """Testa importação de todos os módulos"""
    print("\n7. Testando importação de módulos...")
    
    modulos = [
        ('leitor_pdf', 'LeitorPDF'),
        ('extrator_campos', 'ExtratorCampos'),
        ('extrator_ia', 'ExtratorIA'),
        ('writer_excel', 'WriterExcel'),
        ('writer_sheets', 'WriterSheets'),
        ('monitor_pasta', 'MonitorPasta'),
        ('processador', 'ProcessadorFatura')
    ]
    
    erros = []
    for modulo, classe in modulos:
        try:
            exec(f"from {modulo} import {classe}")
            print(f"   ✓ {modulo}.{classe}")
        except Exception as e:
            print(f"   ✗ {modulo}.{classe}: {str(e)}")
            erros.append((modulo, str(e)))
    
    if erros:
        print("\n   Erros encontrados:")
        for modulo, erro in erros:
            print(f"   - {modulo}: {erro}")
        return False
    
    return True


if __name__ == "__main__":
    print("\n🔧 Iniciando testes do sistema...\n")
    
    # Teste de módulos
    if not teste_modulos():
        print("\n⚠️  Alguns módulos têm problemas. Verifique as dependências.")
        print("   Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Teste básico
    teste_basico()
    
    print("\n✅ Testes concluídos!")
    print("\nPara usar a interface web, execute:")
    print("   streamlit run app.py")
