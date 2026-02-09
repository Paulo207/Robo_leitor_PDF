# 📖 Guia de Uso Detalhado - Robô Leitor de PDFs da Coelba

## Índice
1. [Introdução](#introdução)
2. [Instalação Rápida](#instalação-rápida)
3. [Uso Básico](#uso-básico)
4. [Uso Avançado](#uso-avançado)
5. [Solução de Problemas](#solução-de-problemas)
6. [Perguntas Frequentes](#perguntas-frequentes)

## Introdução

Este robô foi desenvolvido para automatizar a leitura de faturas de energia da Coelba em formato PDF, extraindo automaticamente informações importantes e organizando-as em uma planilha Excel. Isso economiza tempo e reduz erros manuais no processo financeiro.

### O que o robô faz?

1. ✅ Lê arquivos PDF de faturas da Coelba
2. ✅ Extrai automaticamente:
   - Nome do cliente
   - Unidade Consumidora (UC)
   - Mês de referência
   - Data de vencimento
   - Valor total da fatura
   - Consumo em kWh
   - Impostos (ICMS, PIS, COFINS)
3. ✅ Organiza tudo em uma planilha Excel
4. ✅ Processa múltiplas faturas de uma só vez

## Instalação Rápida

### Windows

1. Instale o Python 3.8 ou superior (baixe em python.org)
2. Baixe o projeto e extraia para uma pasta
3. Abra o Prompt de Comando nessa pasta
4. Execute:
```cmd
pip install -r requirements.txt
```

### Linux/Mac

1. Abra o terminal
2. Clone ou baixe o projeto
3. Entre na pasta do projeto:
```bash
cd Robo_leitor_PDF
```
4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso Básico

### Passo 1: Preparar os PDFs

1. Coloque todos os PDFs das faturas da Coelba na pasta `input_pdfs/`
   - A pasta será criada automaticamente na primeira execução
   - Você pode colocar quantos PDFs quiser

### Passo 2: Executar o Robô

Execute o comando:
```bash
python main.py
```

### Passo 3: Verificar o Resultado

1. A planilha será criada em `output/faturas_coelba.xlsx`
2. Abra com Excel, LibreOffice Calc ou Google Sheets
3. Cada linha representa uma fatura processada

### Exemplo de Saída

```
🤖 Robô Leitor de PDFs da Coelba
📁 Pasta de entrada: input_pdfs
📊 Arquivo de saída: output/faturas_coelba.xlsx
📄 Arquivos encontrados: 3

📄 Processando: fatura_janeiro.pdf
✓ Dados extraídos com sucesso
📄 Processando: fatura_fevereiro.pdf
✓ Dados extraídos com sucesso
📄 Processando: fatura_marco.pdf
✓ Dados extraídos com sucesso

✓ Planilha gerada com sucesso: output/faturas_coelba.xlsx
📊 Total de faturas processadas: 3
```

## Uso Avançado

### Especificar Pasta de Entrada Personalizada

```bash
python main.py -i /caminho/para/suas/faturas
```

### Especificar Arquivo de Saída Personalizado

```bash
python main.py -o /caminho/para/resultado.xlsx
```

### Combinando Opções

```bash
python main.py -i ./faturas_2024 -o ./relatorios/janeiro_2024.xlsx
```

### Processar Faturas de Diferentes Períodos

```bash
# Janeiro
python main.py -i faturas_jan -o relatorios/janeiro.xlsx

# Fevereiro
python main.py -i faturas_fev -o relatorios/fevereiro.xlsx

# Março
python main.py -i faturas_mar -o relatorios/marco.xlsx
```

### Usar em Scripts Automatizados

Você pode incluir o robô em scripts de automação:

**Windows (Batch):**
```batch
@echo off
echo Processando faturas...
python main.py -i C:\Faturas\2024 -o C:\Relatorios\faturas_2024.xlsx
if %ERRORLEVEL% EQU 0 (
    echo Sucesso!
) else (
    echo Erro ao processar!
)
```

**Linux/Mac (Bash):**
```bash
#!/bin/bash
echo "Processando faturas..."
python main.py -i ~/Faturas/2024 -o ~/Relatorios/faturas_2024.xlsx
if [ $? -eq 0 ]; then
    echo "Sucesso!"
else
    echo "Erro ao processar!"
fi
```

## Solução de Problemas

### Erro: "Nenhum arquivo PDF encontrado"

**Causa:** A pasta de entrada está vazia ou não contém arquivos PDF.

**Solução:**
1. Verifique se os arquivos estão na pasta correta
2. Verifique se os arquivos têm extensão .pdf (não .PDF.pdf ou outros)
3. Use o caminho completo com `-i` se necessário

### Erro: "Arquivo não encontrado"

**Causa:** O caminho especificado não existe.

**Solução:**
1. Verifique se o caminho está correto
2. Use caminhos absolutos em vez de relativos
3. Verifique se você tem permissões de leitura/escrita

### Dados Não Extraídos Corretamente

**Causa:** O formato do PDF pode ser diferente do esperado.

**Solução:**
1. Verifique se o PDF é realmente da Coelba
2. Tente com outro PDF para confirmar
3. Se o problema persistir, o PDF pode ter um formato não suportado

### Erro de Instalação de Dependências

**Causa:** Problemas com o pip ou versão do Python.

**Solução:**
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências novamente
pip install -r requirements.txt --force-reinstall
```

### Planilha Não Abre

**Causa:** Arquivo corrompido ou Excel não instalado.

**Solução:**
1. Tente abrir com LibreOffice Calc
2. Tente abrir com Google Sheets (upload na web)
3. Verifique se o arquivo realmente foi criado

## Perguntas Frequentes

### 1. O robô funciona com faturas de outras empresas?

Não, ele foi desenvolvido especificamente para o formato da Coelba. Para outras empresas, seria necessário adaptar os padrões de extração.

### 2. Posso processar centenas de PDFs de uma vez?

Sim! O robô foi desenvolvido para processar múltiplos arquivos. Basta colocá-los todos na pasta de entrada.

### 3. Os dados são enviados para algum servidor?

Não! Todo o processamento é local. Nenhum dado é enviado para servidores externos.

### 4. Posso modificar o código para extrair outros campos?

Sim! O código é open source. Você pode modificar `pdf_reader.py` para adicionar novos campos.

### 5. Como posso automatizar o processamento mensal?

Você pode usar ferramentas como:
- Windows: Agendador de Tarefas (Task Scheduler)
- Linux/Mac: Cron jobs
- Python: APScheduler para agendamento dentro do próprio código

### 6. O robô funciona com PDFs escaneados?

Depende. Se o PDF for uma imagem escaneada sem texto, o robô não conseguirá extrair dados. O PDF precisa ter texto selecionável.

### 7. Posso exportar para outros formatos além de Excel?

Atualmente, apenas Excel é suportado. Mas o código pode ser facilmente modificado para suportar CSV, JSON, ou outros formatos.

### 8. O robô usa inteligência artificial?

Ele usa expressões regulares (regex) para extração de dados, que é uma técnica de parsing de texto. Para casos mais complexos, você poderia integrar IA/ML, mas para o caso da Coelba, o parsing por regex é suficiente.

## Exemplos Práticos

### Exemplo 1: Processar Faturas do Ano Todo

```bash
# Criar estrutura de pastas
mkdir -p relatorios/2024

# Processar cada mês
for mes in jan fev mar abr mai jun jul ago set out nov dez; do
    python main.py -i faturas_2024/$mes -o relatorios/2024/$mes.xlsx
done
```

### Exemplo 2: Script Python Personalizado

```python
from pdf_reader import CoelbaPDFReader
from excel_exporter import ExcelExporter

# Processar um PDF específico
reader = CoelbaPDFReader("minha_fatura.pdf")
dados = reader.extract_invoice_data()

# Ver os dados extraídos
print(f"Cliente: {dados['cliente']}")
print(f"Valor: R$ {dados['valor_total']}")

# Salvar em Excel
exporter = ExcelExporter("meu_relatorio.xlsx")
exporter.export_to_excel([dados])
```

### Exemplo 3: Integração com Email

```python
# Exemplo conceitual - requer configuração adicional
import imaplib
import email
from main import CoelbaInvoiceProcessor

# Conectar ao email (Gmail, Outlook, etc)
# Baixar anexos PDF
# Processar com o robô
# Enviar relatório por email
```

## Suporte

Para mais ajuda:
1. Leia o README.md principal
2. Veja o arquivo exemplo.py para exemplos de código
3. Abra uma issue no GitHub se encontrar bugs

## Contribuições

Contribuições são bem-vindas! Se você melhorou o robô ou adicionou funcionalidades, considere fazer um Pull Request.

---

Desenvolvido para simplificar o processo de leitura de faturas de energia ⚡
