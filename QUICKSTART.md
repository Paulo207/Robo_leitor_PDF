# 🚀 Guia de Início Rápido - RPA COELBA

## Instalação em 5 Minutos

### 1️⃣ Pré-requisitos
- Python 3.11 ou superior instalado
- pip atualizado

### 2️⃣ Clone e Configure

```bash
# Clone o repositório
git clone https://github.com/Paulo207/Robo_leitor_PDF.git
cd Robo_leitor_PDF

# Execute o setup automático
python setup.py
```

O script de setup irá:
- ✅ Criar estrutura de pastas
- ✅ Configurar arquivo .env
- ✅ Instalar dependências (se confirmado)
- ✅ Verificar requisitos

### 3️⃣ Configure (Opcional)

Edite o arquivo `.env` se necessário:

```env
# Mínimo necessário para começar
USAR_EXCEL=true
ARQUIVO_EXCEL=faturas_coelba.xlsx
```

### 4️⃣ Execute

```bash
# Interface Web (Recomendado)
streamlit run app.py

# Ou processamento via linha de comando
python teste.py
```

### 5️⃣ Use

1. **Através da Interface Web:**
   - Abra o navegador em `http://localhost:8501`
   - Faça upload de PDFs ou coloque na pasta `entrada_pdfs/`
   - Clique em "Processar" ou ative o monitoramento automático

2. **Através da Pasta Monitorada:**
   - Coloque PDFs em `entrada_pdfs/`
   - Ative o monitoramento na interface
   - Os PDFs serão processados automaticamente

## 🎯 Resultado

Os dados extraídos serão salvos em:
- 📊 `faturas_coelba.xlsx` - Planilha Excel com todos os dados
- 📁 `processados/` - PDFs processados com sucesso
- ❌ `erros/` - PDFs com erro no processamento
- 📝 `logs/` - Logs detalhados

## 📊 Dados Extraídos

Cada fatura terá:
- Nome do Cliente
- Número da UC
- Mês de Referência
- Data de Vencimento
- Valor Total
- Consumo em kWh
- Impostos (ICMS, PIS, COFINS, CIP)

## 🔧 Recursos Opcionais

### OCR para PDFs Escaneados

```bash
# Windows
# Baixe e instale: https://github.com/UB-Mannheim/tesseract/wiki

# Linux
sudo apt-get install tesseract-ocr tesseract-ocr-por

# macOS
brew install tesseract
```

### IA para Melhor Extração

1. Crie conta em: https://platform.openai.com/
2. Gere uma API Key
3. Adicione ao `.env`:
   ```env
   OPENAI_API_KEY=sua_chave_aqui
   ```

### Google Sheets

1. Configure credenciais do Google Cloud
2. Baixe `credentials.json`
3. Configure no `.env`:
   ```env
   USAR_GOOGLE_SHEETS=true
   GOOGLE_SHEET_ID=seu_id
   ```

## 🆘 Problemas Comuns

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Tesseract not found"
- Instale o Tesseract OCR (veja acima)
- Ou desative OCR: `USAR_OCR_FALLBACK=false` no `.env`

### "Campos não encontrados"
- Ajuste `config_campos.json` com labels corretos da sua fatura
- Ou ative IA: `USAR_IA_FALLBACK=true` no `.env`

## 📚 Documentação Completa

- [Manual do Usuário](MANUAL.md) - Guia detalhado
- [README](README.md) - Informações do projeto
- [Exemplos](exemplos.py) - Exemplos de código

## 💡 Dicas

1. **Teste com poucos PDFs primeiro** para calibrar o sistema
2. **Use PDFs com texto nativo** para melhor precisão
3. **Ajuste `config_campos.json`** se os labels da sua fatura forem diferentes
4. **Ative a IA** para preencher campos que regex não conseguir
5. **Consulte os logs** em `logs/processamento.log` para depuração

## ✨ Pronto!

Seu sistema RPA está configurado e pronto para processar faturas da COELBA automaticamente!

Para mais ajuda, consulte o [Manual Completo](MANUAL.md).
