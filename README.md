# 🤖 Robô Leitor de PDFs da Coelba

Robô automatizado para leitura e extração de dados de faturas de energia da Coelba em PDF. O sistema processa automaticamente os arquivos PDF, extrai informações importantes e organiza tudo em uma planilha Excel.

## 📋 Funcionalidades

- **Leitura Automática de PDFs**: Processa múltiplos arquivos PDF de faturas da Coelba
- **Extração Inteligente de Dados**: Captura automaticamente:
  - Nome do cliente
  - Unidade Consumidora (UC)
  - Mês de referência
  - Data de vencimento
  - Valor total
  - Consumo em kWh
  - Impostos (ICMS, PIS, COFINS)
- **Exportação para Excel**: Organiza todos os dados em planilha com uma linha por fatura
- **Redução de Erros**: Elimina erros de digitação manual
- **Economia de Tempo**: Processa automaticamente múltiplas faturas

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Paulo207/Robo_leitor_PDF.git
cd Robo_leitor_PDF
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Uso Básico

1. Coloque os arquivos PDF das faturas da Coelba na pasta `input_pdfs/` (será criada automaticamente)

2. Execute o robô:
```bash
python main.py
```

3. A planilha será gerada em `output/faturas_coelba.xlsx`

### Uso Avançado

Você pode especificar pastas personalizadas:

```bash
python main.py -i /caminho/para/pdfs -o /caminho/saida/planilha.xlsx
```

#### Opções de linha de comando:

- `-i, --input`: Pasta contendo os PDFs (padrão: `input_pdfs`)
- `-o, --output`: Arquivo Excel de saída (padrão: `output/faturas_coelba.xlsx`)
- `-h, --help`: Exibe ajuda

### Exemplo de Uso

```bash
# Processar PDFs da pasta 'faturas_2024' e salvar em 'resultados/janeiro.xlsx'
python main.py -i faturas_2024 -o resultados/janeiro.xlsx
```

## 📊 Estrutura da Planilha

A planilha Excel gerada contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| arquivo | Nome do arquivo PDF processado |
| cliente | Nome do cliente |
| uc | Número da Unidade Consumidora |
| mes_referencia | Mês/ano de referência da fatura |
| vencimento | Data de vencimento |
| valor_total | Valor total da fatura (R$) |
| consumo_kwh | Consumo em kWh |
| impostos | Valores de impostos (ICMS, PIS, COFINS) |

## 🏗️ Estrutura do Projeto

```
Robo_leitor_PDF/
├── main.py              # Script principal
├── pdf_reader.py        # Módulo de leitura e extração de PDFs
├── excel_exporter.py    # Módulo de exportação para Excel
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
├── .gitignore          # Arquivos ignorados pelo Git
├── input_pdfs/         # Pasta para arquivos PDF (criada automaticamente)
└── output/             # Pasta para arquivos de saída (criada automaticamente)
```

## 🔧 Módulos

### pdf_reader.py
Responsável por:
- Abrir e ler arquivos PDF
- Extrair texto usando pdfplumber
- Identificar e extrair dados específicos usando expressões regulares

### excel_exporter.py
Responsável por:
- Criar planilhas Excel
- Formatar dados extraídos
- Adicionar novas faturas a planilhas existentes

### main.py
Responsável por:
- Interface de linha de comando
- Coordenar o processamento
- Gerenciar arquivos de entrada e saída

## 📦 Dependências

- **PyPDF2**: Manipulação de arquivos PDF
- **pdfplumber**: Extração avançada de texto de PDFs
- **pandas**: Manipulação de dados
- **openpyxl**: Criação e edição de arquivos Excel
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📝 Melhorias Futuras

- [ ] Integração com e-mail para captura automática de faturas
- [ ] Suporte para Google Sheets
- [ ] Interface gráfica (GUI)
- [ ] Uso de IA/Machine Learning para melhor extração
- [ ] Suporte para outras companhias de energia
- [ ] Validação automática de dados extraídos
- [ ] Relatórios de consumo e análises

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

Paulo207

## 🙏 Agradecimentos

Desenvolvido para automatizar e simplificar o processo de leitura de faturas de energia, economizando tempo e reduzindo erros no processo financeiro.