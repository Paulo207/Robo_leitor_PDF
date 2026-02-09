# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o projeto RPA COELBA! 

## Como Contribuir

### Reportar Bugs

Se você encontrar um bug:

1. Verifique se já não existe uma issue sobre o problema
2. Abra uma nova issue incluindo:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Versão do Python
   - Sistema operacional
   - Logs relevantes (de `logs/processamento.log`)

### Sugerir Melhorias

Para sugerir novas funcionalidades:

1. Verifique se já não existe uma issue similar
2. Abra uma nova issue com:
   - Descrição clara da funcionalidade
   - Justificativa (por que seria útil)
   - Exemplos de uso
   - Possível implementação (se aplicável)

### Contribuir com Código

1. **Fork o repositório**

2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/Robo_leitor_PDF.git
   cd Robo_leitor_PDF
   ```

3. **Crie uma branch**
   ```bash
   git checkout -b feature/minha-funcionalidade
   # ou
   git checkout -b fix/correcao-bug
   ```

4. **Faça suas alterações**
   - Siga o estilo de código existente
   - Adicione comentários quando necessário
   - Mantenha o código limpo e legível

5. **Teste suas alterações**
   ```bash
   python teste.py
   streamlit run app.py
   ```

6. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "Adiciona/Corrige: descrição clara"
   ```

7. **Push para seu fork**
   ```bash
   git push origin feature/minha-funcionalidade
   ```

8. **Abra um Pull Request**
   - Descreva claramente as mudanças
   - Referencie issues relacionadas
   - Aguarde review

## Padrões de Código

### Estilo Python

- Siga PEP 8
- Use type hints quando possível
- Docstrings para funções e classes
- Nomes descritivos para variáveis

```python
def extrair_campo(texto: str, nome_campo: str) -> Optional[str]:
    """
    Extrai um campo específico do texto
    
    Args:
        texto: Texto do PDF
        nome_campo: Nome do campo a extrair
        
    Returns:
        Valor extraído ou None
    """
    # implementação
    pass
```

### Organização de Código

- Um módulo por responsabilidade
- Funções pequenas e focadas
- Evite código duplicado
- Trate exceções adequadamente

### Logging

Use logging ao invés de print:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Mensagem informativa")
logger.warning("Aviso")
logger.error("Erro")
```

## Estrutura do Projeto

```
/Robo_leitor_PDF
├── app.py              # Interface Streamlit
├── processador.py      # Orquestrador
├── leitor_pdf.py       # Leitura de PDFs
├── extrator_campos.py  # Extração regex
├── extrator_ia.py      # Extração IA
├── writer_excel.py     # Saída Excel
├── writer_sheets.py    # Saída Sheets
├── monitor_pasta.py    # Monitoramento
└── config_campos.json  # Configuração
```

## Áreas que Precisam de Ajuda

- 🐛 Correção de bugs
- 📝 Melhorias na documentação
- 🧪 Testes automatizados
- 🌐 Suporte a outras concessionárias
- 🎨 Melhorias na interface
- ⚡ Otimizações de performance
- 🔧 Novos recursos

## Diretrizes de Pull Request

### O que incluir:

- ✅ Descrição clara das mudanças
- ✅ Testes (se aplicável)
- ✅ Documentação atualizada
- ✅ Código comentado quando necessário
- ✅ Changelog entry (se relevante)

### O que evitar:

- ❌ Mudanças não relacionadas no mesmo PR
- ❌ Código sem testes para novas funcionalidades
- ❌ Quebrar funcionalidades existentes
- ❌ Commits com mensagens vagas

## Processo de Review

1. Mantainer revisa o código
2. Pode solicitar mudanças
3. Discussão se necessário
4. Aprovação e merge

## Dúvidas?

- Abra uma issue com a tag `question`
- Veja a documentação em `MANUAL.md`
- Consulte exemplos em `exemplos.py`

## Código de Conduta

- Seja respeitoso e construtivo
- Ajude outros contribuidores
- Foque em melhorar o projeto
- Aceite feedback com profissionalismo

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

---

**Obrigado por contribuir! 🎉**
