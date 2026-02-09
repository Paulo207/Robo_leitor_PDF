# 📘 Manual do Usuário - RPA COELBA

## Sistema de Leitura Automatizada de Faturas de Energia

---

## 📋 Índice

1. [Introdução](#introdução)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Como Usar](#como-usar)
6. [Solução de Problemas](#solução-de-problemas)
7. [Perguntas Frequentes](#perguntas-frequentes)

---

## 🎯 Introdução

O RPA COELBA é um sistema automatizado que lê faturas de energia da COELBA em formato PDF e extrai automaticamente informações importantes, salvando-as em planilhas Excel ou Google Sheets.

### Principais Funcionalidades

- ✅ Leitura automática de PDFs (texto nativo e escaneados via OCR)
- ✅ Extração de 10+ campos importantes
- ✅ Salvamento em Excel ou Google Sheets
- ✅ Monitoramento automático de pasta
- ✅ Interface web amigável
- ✅ Sistema de logs e auditoria
- ✅ Organização automática de arquivos

### Campos Extraídos

- Nome do Cliente
- Número da UC (Unidade Consumidora)
- Mês de Referência
- Data de Vencimento
- Valor Total da Fatura
- Consumo em kWh
- Impostos (ICMS, PIS, COFINS, CIP)

---

## 💻 Requisitos do Sistema

### Hardware

- Processador: Intel Core i3 ou superior
- RAM: 4GB mínimo (8GB recomendado)
- Espaço em disco: 500MB livres

### Software

- Windows 10/11 (ou Linux/macOS)
- Python 3.11 ou superior
- Tesseract OCR (para PDFs escaneados)

---

## 🚀 Instalação

### Passo 1: Instalar Python

1. Baixe Python em: https://www.python.org/downloads/
2. Durante a instalação, marque "Add Python to PATH"
3. Verifique a instalação:
   ```bash
   python --version
   ```

### Passo 2: Instalar Tesseract OCR (Opcional)

Para processar PDFs escaneados:

**Windows:**
1. Baixe em: https://github.com/UB-Mannheim/tesseract/wiki
2. Instale o executável
3. Adicione ao PATH do sistema

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-por
```

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang
```

### Passo 3: Instalar Dependências do Sistema

1. Abra o terminal/prompt na pasta do projeto
2. Execute:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuração

### Configuração Básica

1. Copie o arquivo de exemplo:
   ```bash
   copy .env.example .env
   ```

2. Edite o arquivo `.env` com suas configurações:

```env
# Configurações de Pastas
PASTA_ENTRADA=entrada_pdfs
PASTA_PROCESSADOS=processados
PASTA_ERROS=erros
PASTA_LOGS=logs

# Saída
USAR_EXCEL=true
USAR_GOOGLE_SHEETS=false
ARQUIVO_EXCEL=faturas_coelba.xlsx

# Processamento
USAR_IA_FALLBACK=true
USAR_OCR_FALLBACK=true
VALIDAR_VALORES=true
RENOMEAR_ARQUIVOS=true
```

### Configuração do Google Sheets (Opcional)

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto
3. Ative a API do Google Sheets
4. Crie credenciais (Service Account)
5. Baixe o arquivo JSON e salve como `credentials.json` na pasta do projeto
6. No arquivo `.env`, configure:
   ```env
   USAR_GOOGLE_SHEETS=true
   GOOGLE_SHEET_ID=seu_id_da_planilha
   ```

### Configuração da IA (Opcional)

Para usar IA como fallback:

1. Crie uma conta em: https://platform.openai.com/
2. Gere uma API Key
3. Adicione ao `.env`:
   ```env
   OPENAI_API_KEY=sua_chave_aqui
   OPENAI_MODEL=gpt-3.5-turbo
   ```

---

## 📖 Como Usar

### Método 1: Interface Web (Recomendado)

1. Inicie a aplicação:
   ```bash
   streamlit run app.py
   ```

2. O navegador abrirá automaticamente em `http://localhost:8501`

3. Na interface:
   - **Dashboard**: Veja o status do sistema
   - **Processamento**: Processe PDFs manualmente ou faça upload
   - **Estatísticas**: Veja relatórios e dados processados
   - **Logs**: Acompanhe o histórico de processamento

### Método 2: Processamento por Pasta

1. Coloque os PDFs na pasta `entrada_pdfs/`
2. Na interface, clique em "Iniciar Monitoramento"
3. O sistema processará automaticamente novos arquivos

### Método 3: Upload Manual

1. Na aba "Processamento"
2. Clique em "Upload de PDF"
3. Selecione o arquivo
4. Clique em "Processar Agora"

---

## 🔧 Solução de Problemas

### Problema: "Não foi possível extrair texto"

**Soluções:**
- Verifique se o Tesseract OCR está instalado
- Confirme que o PDF não está corrompido
- Teste abrir o PDF em um leitor convencional

### Problema: "Campos não encontrados"

**Soluções:**
- Ajuste o arquivo `config_campos.json` com os labels corretos
- Ative a opção "Usar IA como fallback"
- Verifique se a fatura é realmente da COELBA

### Problema: "Erro ao salvar no Excel"

**Soluções:**
- Feche o arquivo Excel se estiver aberto
- Verifique permissões da pasta
- Recrie o arquivo Excel clicando em "Processar Todos"

### Problema: "Google Sheets não funciona"

**Soluções:**
- Verifique se o arquivo `credentials.json` existe
- Confirme que a API do Google Sheets está ativada
- Verifique o ID da planilha no `.env`
- Dê permissão de edição à Service Account

---

## ❓ Perguntas Frequentes

### Como adicionar novos campos para extração?

Edite o arquivo `config_campos.json` e adicione:

```json
{
  "novo_campo": {
    "labels": ["LABEL NO PDF", "ALTERNATIVA"],
    "tipo": "texto",
    "obrigatorio": false,
    "pattern": "regex_pattern"
  }
}
```

### Como evitar duplicatas?

O sistema verifica automaticamente por UC + Mês de Referência. Arquivos duplicados são marcados e movidos para a pasta `processados` com sufixo `_duplicata`.

### Posso processar faturas de outras concessionárias?

Sim! Basta ajustar o arquivo `config_campos.json` com os labels específicos da sua concessionária.

### Como fazer backup dos dados?

- **Excel**: Copie o arquivo `faturas_coelba.xlsx`
- **Google Sheets**: Os dados já estão na nuvem
- **Logs**: Copie a pasta `logs/`

### O sistema funciona offline?

Sim, exceto:
- Integração com Google Sheets (requer internet)
- IA como fallback (requer internet)
- OCR funciona offline após instalação

### Como melhorar a precisão da extração?

1. Use PDFs com texto nativo (não escaneados)
2. Ajuste os labels em `config_campos.json`
3. Ative a IA como fallback
4. Forneça exemplos de faturas para calibrar o sistema

### Quantos PDFs posso processar por vez?

Não há limite técnico. O sistema foi testado com:
- ✅ 100 PDFs: ~5-10 minutos
- ✅ 1000 PDFs: ~1-2 horas

### Como processar PDFs antigos?

Coloque todos os PDFs na pasta `entrada_pdfs` e clique em "Processar Todos os PDFs" na interface.

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `logs/processamento.log`
2. Consulte este manual
3. Abra uma issue no repositório do projeto

---

## 📄 Licença

Este sistema foi desenvolvido para uso interno e educacional.

---

**Última atualização:** 2024
**Versão:** 1.0.0
