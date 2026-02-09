"""
Script de instalação e configuração inicial do sistema RPA COELBA
"""

import os
import sys
from pathlib import Path
import shutil


def criar_env():
    """Cria arquivo .env se não existir"""
    print("📝 Configurando arquivo .env...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("   ℹ Arquivo .env já existe")
        resposta = input("   Deseja sobrescrever? (s/n): ")
        if resposta.lower() != 's':
            print("   ⏭ Mantendo arquivo existente")
            return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("   ✓ Arquivo .env criado com sucesso")
    else:
        print("   ✗ Arquivo .env.example não encontrado")


def criar_pastas():
    """Cria estrutura de pastas necessárias"""
    print("\n📁 Criando estrutura de pastas...")
    
    pastas = ['entrada_pdfs', 'processados', 'erros', 'logs']
    
    for pasta in pastas:
        path = Path(pasta)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"   ✓ Pasta '{pasta}' criada")
        else:
            print(f"   ℹ Pasta '{pasta}' já existe")


def verificar_python():
    """Verifica versão do Python"""
    print("\n🐍 Verificando Python...")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("   ⚠️  Python 3.11+ recomendado")
        return False
    else:
        print("   ✓ Versão adequada")
        return True


def instalar_dependencias():
    """Instala dependências do requirements.txt"""
    print("\n📦 Instalando dependências...")
    
    resposta = input("   Deseja instalar as dependências agora? (s/n): ")
    
    if resposta.lower() == 's':
        print("   ⏳ Instalando... (isso pode levar alguns minutos)")
        
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("   ✓ Dependências instaladas com sucesso")
                return True
            else:
                print("   ✗ Erro na instalação:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"   ✗ Erro: {str(e)}")
            return False
    else:
        print("   ⏭ Instalação pulada")
        print("   💡 Execute manualmente: pip install -r requirements.txt")
        return False


def verificar_tesseract():
    """Verifica se Tesseract OCR está instalado"""
    print("\n👁️ Verificando Tesseract OCR...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"   ✓ {version}")
            return True
        else:
            print("   ✗ Tesseract não encontrado")
            return False
            
    except Exception:
        print("   ✗ Tesseract não instalado")
        print("   💡 Para processar PDFs escaneados, instale:")
        print("      Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("      Linux: sudo apt-get install tesseract-ocr tesseract-ocr-por")
        print("      macOS: brew install tesseract")
        return False


def mostrar_proximos_passos():
    """Mostra os próximos passos para o usuário"""
    print("\n" + "=" * 60)
    print("✅ CONFIGURAÇÃO INICIAL CONCLUÍDA")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASSOS:\n")
    
    print("1. Configure o arquivo .env com suas preferências:")
    print("   - Edite o arquivo .env no editor de texto")
    print("   - Adicione sua OpenAI API key (opcional)")
    print("   - Configure Google Sheets (opcional)")
    
    print("\n2. Coloque PDFs de faturas COELBA na pasta 'entrada_pdfs'")
    
    print("\n3. Execute a aplicação:")
    print("   streamlit run app.py")
    
    print("\n4. Ou teste o processamento:")
    print("   python teste.py")
    
    print("\n" + "=" * 60)
    print("\n💡 Consulte MANUAL.md para mais informações\n")


def main():
    """Função principal de setup"""
    print("=" * 60)
    print("🚀 SETUP DO SISTEMA RPA COELBA")
    print("=" * 60)
    
    # Verificar Python
    verificar_python()
    
    # Criar estrutura
    criar_pastas()
    criar_env()
    
    # Instalar dependências
    deps_ok = instalar_dependencias()
    
    # Verificar Tesseract
    verificar_tesseract()
    
    # Próximos passos
    mostrar_proximos_passos()


if __name__ == "__main__":
    main()
