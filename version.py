"""
Informações de versão do sistema RPA COELBA
"""

__version__ = "1.0.0"
__author__ = "Paulo207"
__description__ = "Sistema RPA para leitura automatizada de faturas COELBA"
__license__ = "MIT"

# Informações do projeto
PROJECT_NAME = "RPA COELBA - Leitor de Faturas"
PROJECT_URL = "https://github.com/Paulo207/Robo_leitor_PDF"
DOCUMENTATION_URL = "https://github.com/Paulo207/Robo_leitor_PDF/blob/main/MANUAL.md"

# Versões de componentes
PYTHON_MIN_VERSION = "3.11"
STREAMLIT_VERSION = "1.29.0"

# Metadados
SUPPORTED_PDF_TYPES = ["text", "scanned"]
SUPPORTED_OUTPUT_FORMATS = ["excel", "google_sheets"]
SUPPORTED_COMPANIES = ["COELBA"]

# Configurações padrão
DEFAULT_CONFIG = {
    "pasta_entrada": "entrada_pdfs",
    "pasta_processados": "processados",
    "pasta_erros": "erros",
    "pasta_logs": "logs",
    "arquivo_excel": "faturas_coelba.xlsx",
    "usar_ocr": True,
    "usar_ia": True,
    "validar_valores": True,
    "renomear_arquivos": True
}


def get_version_info():
    """Retorna informações de versão formatadas"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "license": __license__,
        "project_name": PROJECT_NAME,
        "project_url": PROJECT_URL,
        "python_min": PYTHON_MIN_VERSION
    }


def print_version():
    """Imprime informações de versão"""
    print(f"{PROJECT_NAME} v{__version__}")
    print(f"Autor: {__author__}")
    print(f"Licença: {__license__}")
    print(f"URL: {PROJECT_URL}")


if __name__ == "__main__":
    print_version()
