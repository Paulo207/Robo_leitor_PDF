# ⚡ RPA COELBA - Sistema de Leitura Automatizada de Faturas

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Sistema RPA (Robotic Process Automation) com IA para leitura automática de faturas de energia da COELBA em PDF, extração de campos específicos e armazenamento em Excel ou Google Sheets.

## 🎯 Características Principais

- 🤖 **Automação Completa**: Monitoramento de pasta e processamento automático
- 🧠 **IA Integrada**: Fallback com OpenAI para extração de campos
- 👁️ **OCR Avançado**: Suporte para PDFs escaneados via Tesseract
- 📊 **Múltiplas Saídas**: Excel local ou Google Sheets
- 🎨 **Interface Web**: Painel Streamlit intuitivo e responsivo
- 📈 **Dashboard**: Estatísticas e métricas em tempo real
- 🔍 **Rastreabilidade**: Sistema completo de logs e auditoria
- 🔧 **Configurável**: Ajuste campos via JSON sem alterar código

## 📋 Campos Extraídos

- Nome do Cliente
- Número da UC (Unidade Consumidora)
- Mês de Referência
- Data de Vencimento
- Valor Total da Fatura
- Consumo em kWh
- Impostos: ICMS, PIS, COFINS, CIP

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Tesseract OCR (opcional, para PDFs escaneados)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Paulo207/Robo_leitor_PDF.git
cd Robo_leitor_PDF

# Instale as dependências
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute a aplicação
streamlit run app.py
```

A interface abrirá automaticamente em `http://localhost:8501`

## 📖 Uso

### 1. Interface Web (Recomendado)

Execute `streamlit run app.py` e use a interface para:
- Monitorar pasta automaticamente
- Fazer upload manual de PDFs
- Processar arquivos existentes
- Visualizar estatísticas e logs

### 2. Processamento por Pasta

```python
from processador import ProcessadorFatura

# Criar processador
processador = ProcessadorFatura()

# Processar um PDF
sucesso, dados = processador.processar_pdf("caminho/para/fatura.pdf")
```

### 3. Monitoramento Automático

```python
from monitor_pasta import MonitorPasta
from processador import ProcessadorFatura

processador = ProcessadorFatura()
monitor = MonitorPasta("entrada_pdfs", processador.processar_pdf)

# Iniciar monitoramento
monitor.iniciar()
monitor.processar_existentes()
monitor.aguardar()
```

## 🏗️ Arquitetura

```
/Robo_leitor_PDF
│
├── app.py                    # Interface Streamlit
├── processador.py            # Orquestrador principal
├── leitor_pdf.py            # Extração de texto (PDF + OCR)
├── extrator_campos.py       # Extração com regex
├── extrator_ia.py           # Extração com IA (fallback)
├── writer_excel.py          # Gravação em Excel
├── writer_sheets.py         # Gravação em Google Sheets
├── monitor_pasta.py         # Monitoramento de diretório
├── config_campos.json       # Configuração de campos
├── requirements.txt         # Dependências
├── .env                     # Configurações do sistema
│
├── /entrada_pdfs           # PDFs a processar
├── /processados            # PDFs processados com sucesso
├── /erros                  # PDFs com erro
└── /logs                   # Logs do sistema
```

## ⚙️ Configuração

### Arquivo .env

```env
# Pastas
PASTA_ENTRADA=entrada_pdfs
PASTA_PROCESSADOS=processados
PASTA_ERROS=erros
PASTA_LOGS=logs

# Saída
USAR_EXCEL=true
USAR_GOOGLE_SHEETS=false
ARQUIVO_EXCEL=faturas_coelba.xlsx

# Google Sheets (opcional)
GOOGLE_SHEET_ID=
GOOGLE_SHEET_ABA=Faturas

# OpenAI (opcional)
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

# Processamento
USAR_IA_FALLBACK=true
USAR_OCR_FALLBACK=true
VALIDAR_VALORES=true
RENOMEAR_ARQUIVOS=true
```

### Configuração de Campos (config_campos.json)

Personalize os labels e padrões de extração:

```json
{
  "campo_configuracoes": {
    "valor_total": {
      "labels": ["VALOR TOTAL", "TOTAL A PAGAR"],
      "tipo": "monetario",
      "obrigatorio": true,
      "pattern": "R?\\$?\\s*\\d{1,3}(?:\\.\\d{3})*,\\d{2}"
    }
  }
}
```

## 🎨 Capturas de Tela

### Dashboard
Interface principal com métricas em tempo real, status das pastas e controle de monitoramento.

### Processamento
Upload de arquivos, processamento em lote e barra de progresso.

### Estatísticas
Relatórios detalhados com valores totais, médias e histórico de faturas.

## 📊 Fluxo de Processamento

```
1. PDF adicionado → entrada_pdfs/
2. Detecção automática (se monitoramento ativo)
3. Validação do PDF
4. Extração de texto (nativo ou OCR)
5. Extração de campos (regex)
6. IA fallback (se necessário)
7. Validação de campos obrigatórios
8. Verificação de duplicatas
9. Salvamento (Excel/Sheets)
10. Organização: PDF → processados/ ou erros/
11. Registro em logs
```

## 🧪 Testes

O sistema foi testado com:
- ✅ PDFs com texto nativo
- ✅ PDFs escaneados (OCR)
- ✅ Lotes de 100+ faturas
- ✅ Detecção de duplicatas
- ✅ Validação de valores

## 🛠️ Tecnologias

- **Python 3.11+**: Linguagem principal
- **Streamlit**: Interface web
- **pdfplumber**: Extração de texto de PDFs
- **Tesseract OCR**: OCR para PDFs escaneados
- **pandas/openpyxl**: Manipulação de Excel
- **gspread**: Integração com Google Sheets
- **OpenAI API**: IA para extração (opcional)
- **watchdog**: Monitoramento de arquivos

## 📚 Documentação

- [Manual do Usuário](MANUAL.md) - Guia completo de uso
- [Configuração de Campos](config_campos.json) - Personalização de extração

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como solução RPA para automação de leitura de faturas de energia.

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores das bibliotecas utilizadas
- COELBA (contexto do projeto)

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte o [Manual do Usuário](MANUAL.md)
- Abra uma [Issue](https://github.com/Paulo207/Robo_leitor_PDF/issues)
- Verifique os logs em `logs/processamento.log`

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!