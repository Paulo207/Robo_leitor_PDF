# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2024-02-09

### Adicionado
- Sistema RPA completo para leitura de faturas COELBA
- Módulo de leitura de PDFs (`leitor_pdf.py`)
  - Suporte para PDFs com texto nativo via pdfplumber
  - Fallback OCR com Tesseract para PDFs escaneados
- Módulo de extração de campos (`extrator_campos.py`)
  - Extração via regex configurável
  - Busca por proximidade de labels
  - Validação de campos obrigatórios
- Módulo de extração com IA (`extrator_ia.py`)
  - Integração com OpenAI GPT
  - Fallback inteligente para campos não encontrados
  - Melhoria automática de extrações incompletas
- Módulo de escrita em Excel (`writer_excel.py`)
  - Criação automática de planilha modelo
  - Formatação profissional de cabeçalhos
  - Verificação de duplicatas
  - Estatísticas de processamento
- Módulo de escrita em Google Sheets (`writer_sheets.py`)
  - Integração com Google Sheets API
  - Autenticação via Service Account
  - Processamento em lote eficiente
- Módulo de monitoramento (`monitor_pasta.py`)
  - Monitoramento automático de pasta via watchdog
  - Processamento em tempo real de novos PDFs
  - Processamento de arquivos existentes
- Orquestrador principal (`processador.py`)
  - Fluxo completo de processamento
  - Organização automática de arquivos
  - Sistema de logs robusto
  - Validação e tratamento de erros
- Interface web com Streamlit (`app.py`)
  - Dashboard com métricas em tempo real
  - Upload manual de PDFs
  - Processamento em lote
  - Visualização de estatísticas
  - Logs do sistema
  - Controle de monitoramento
- Arquivo de configuração (`config_campos.json`)
  - Configuração flexível de campos
  - Patterns regex customizáveis
  - Labels alternativos por campo
- Documentação completa
  - Manual do usuário (`MANUAL.md`)
  - Guia de início rápido (`QUICKSTART.md`)
  - Guia de contribuição (`CONTRIBUTING.md`)
  - Exemplos de uso (`exemplos.py`)
  - README detalhado
- Scripts auxiliares
  - Script de setup (`setup.py`)
  - Script de teste (`teste.py`)
- Estrutura de pastas organizada
  - `entrada_pdfs/` - PDFs para processar
  - `processados/` - PDFs processados com sucesso
  - `erros/` - PDFs com erro
  - `logs/` - Logs do sistema
- Licença MIT
- `.gitignore` configurado
- Arquivo `.env.example` com configurações padrão

### Campos Extraídos
- Nome do Cliente
- Número da UC (Unidade Consumidora)
- Mês de Referência
- Data de Vencimento
- Valor Total da Fatura
- Consumo em kWh
- ICMS
- PIS
- COFINS
- CIP

### Funcionalidades
- ✅ Processamento automático via monitoramento de pasta
- ✅ Processamento manual via interface web
- ✅ Upload direto de PDFs
- ✅ Suporte a PDFs texto e escaneados
- ✅ Extração híbrida (regex + IA)
- ✅ Múltiplos formatos de saída (Excel, Google Sheets)
- ✅ Detecção de duplicatas
- ✅ Renomeação inteligente de arquivos
- ✅ Sistema completo de logs
- ✅ Estatísticas e métricas
- ✅ Dashboard visual
- ✅ Configuração via JSON e .env

### Tecnologias
- Python 3.11+
- Streamlit
- pdfplumber
- Tesseract OCR
- pandas/openpyxl
- gspread
- OpenAI API
- watchdog

---

## [Não Lançado]

### Planejado
- [ ] Testes automatizados
- [ ] Suporte a outras concessionárias
- [ ] API REST
- [ ] Docker container
- [ ] Executável standalone (.exe)
- [ ] Dashboard de consumo com gráficos
- [ ] Alertas de vencimento
- [ ] Multi-empresa
- [ ] Integração com e-mail (IMAP/Gmail API)
- [ ] Relatórios PDF

---

## Formato de Versionamento

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades (compatível)
- **PATCH**: Correções de bugs (compatível)

## Tipos de Mudanças

- **Adicionado**: Novas funcionalidades
- **Alterado**: Mudanças em funcionalidades existentes
- **Descontinuado**: Funcionalidades que serão removidas
- **Removido**: Funcionalidades removidas
- **Corrigido**: Correções de bugs
- **Segurança**: Correções de vulnerabilidades
