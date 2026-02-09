"""
Interface Streamlit para o sistema RPA de leitura de faturas COELBA
"""

import streamlit as st
import logging
from pathlib import Path
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import sys

from processador import ProcessadorFatura
from monitor_pasta import MonitorPasta
from writer_excel import WriterExcel

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="RPA COELBA - Leitor de Faturas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def inicializar_sessao():
    """Inicializa variáveis de sessão"""
    if 'processador' not in st.session_state:
        st.session_state.processador = ProcessadorFatura()
    
    if 'monitor' not in st.session_state:
        st.session_state.monitor = None
    
    if 'monitoramento_ativo' not in st.session_state:
        st.session_state.monitoramento_ativo = False
    
    if 'logs' not in st.session_state:
        st.session_state.logs = []


def adicionar_log(mensagem: str, tipo: str = "info"):
    """Adiciona mensagem ao log da interface"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.logs.insert(0, {
        'timestamp': timestamp,
        'tipo': tipo,
        'mensagem': mensagem
    })
    # Manter apenas últimos 50 logs
    st.session_state.logs = st.session_state.logs[:50]


def processar_arquivo_callback(caminho_pdf: str):
    """Callback para processar arquivo"""
    sucesso, dados = st.session_state.processador.processar_pdf(caminho_pdf)
    
    if sucesso:
        adicionar_log(f"✅ {Path(caminho_pdf).name} processado com sucesso", "success")
    else:
        adicionar_log(f"❌ Erro ao processar {Path(caminho_pdf).name}", "error")


def main():
    """Função principal da interface"""
    
    # Inicializar sessão
    inicializar_sessao()
    
    # Título e descrição
    st.title("⚡ RPA COELBA - Leitor de Faturas de Energia")
    st.markdown("Sistema automatizado para leitura e processamento de faturas de energia da COELBA")
    
    # Sidebar - Configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Pasta de entrada
        pasta_entrada = st.text_input(
            "Pasta de Entrada",
            value=os.getenv('PASTA_ENTRADA', 'entrada_pdfs'),
            help="Pasta onde os PDFs serão colocados"
        )
        
        # Opções de saída
        st.subheader("Saída de Dados")
        usar_excel = st.checkbox("Usar Excel", value=True)
        usar_sheets = st.checkbox("Usar Google Sheets", value=False)
        
        if usar_excel:
            arquivo_excel = st.text_input(
                "Arquivo Excel",
                value=os.getenv('ARQUIVO_EXCEL', 'faturas_coelba.xlsx')
            )
        
        # Opções de processamento
        st.subheader("Processamento")
        usar_ia = st.checkbox("Usar IA como fallback", value=True, 
                             help="Usar IA para preencher campos não encontrados por regex")
        usar_ocr = st.checkbox("Usar OCR para PDFs escaneados", value=True)
        validar = st.checkbox("Validar valores", value=True)
        renomear = st.checkbox("Renomear arquivos processados", value=True)
        
        st.divider()
        
        # Botão de resetar estatísticas
        if st.button("🔄 Resetar Estatísticas"):
            st.session_state.processador.resetar_estatisticas()
            st.success("Estatísticas resetadas!")
    
    # Layout principal em tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "🤖 Processamento", 
        "📈 Estatísticas",
        "📋 Logs"
    ])
    
    # Tab 1 - Dashboard
    with tab1:
        st.header("Status do Sistema")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        stats = st.session_state.processador.obter_estatisticas()
        
        with col1:
            st.metric("Total Processado", stats['total'])
        
        with col2:
            st.metric("Sucesso", stats['sucesso'], delta=None, delta_color="normal")
        
        with col3:
            st.metric("Erros", stats['erro'], delta=None, delta_color="inverse")
        
        with col4:
            st.metric("Duplicatas", stats['duplicatas'])
        
        st.divider()
        
        # Status de pastas
        st.subheader("📁 Status das Pastas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pasta_ent = Path(pasta_entrada)
            num_entrada = len(list(pasta_ent.glob('*.pdf'))) if pasta_ent.exists() else 0
            st.info(f"**Entrada:** {num_entrada} PDFs pendentes")
        
        with col2:
            pasta_proc = Path('processados')
            num_proc = len(list(pasta_proc.glob('*.pdf'))) if pasta_proc.exists() else 0
            st.success(f"**Processados:** {num_proc} PDFs")
        
        with col3:
            pasta_err = Path('erros')
            num_err = len(list(pasta_err.glob('*.pdf'))) if pasta_err.exists() else 0
            st.error(f"**Erros:** {num_err} PDFs")
        
        st.divider()
        
        # Monitoramento automático
        st.subheader("👁️ Monitoramento Automático")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.session_state.monitoramento_ativo:
                if st.button("⏸️ Parar Monitoramento", type="secondary"):
                    if st.session_state.monitor:
                        st.session_state.monitor.parar()
                        st.session_state.monitoramento_ativo = False
                        adicionar_log("Monitoramento parado", "info")
                        st.rerun()
            else:
                if st.button("▶️ Iniciar Monitoramento", type="primary"):
                    st.session_state.monitor = MonitorPasta(
                        pasta_entrada, 
                        processar_arquivo_callback
                    )
                    st.session_state.monitor.iniciar()
                    st.session_state.monitoramento_ativo = True
                    adicionar_log("Monitoramento iniciado", "success")
                    st.rerun()
        
        with col2:
            if st.session_state.monitoramento_ativo:
                st.success("🟢 Monitoramento ATIVO - Novos PDFs serão processados automaticamente")
            else:
                st.warning("🔴 Monitoramento INATIVO")
    
    # Tab 2 - Processamento
    with tab2:
        st.header("Processamento Manual")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Processar Arquivos Existentes")
            st.write("Processa todos os PDFs que já estão na pasta de entrada")
            
            if st.button("🚀 Processar Todos os PDFs", type="primary", use_container_width=True):
                pasta = Path(pasta_entrada)
                pdfs = list(pasta.glob('*.pdf'))
                
                if not pdfs:
                    st.warning("Nenhum PDF encontrado na pasta de entrada")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, pdf in enumerate(pdfs):
                        status_text.text(f"Processando {i+1}/{len(pdfs)}: {pdf.name}")
                        
                        sucesso, _ = st.session_state.processador.processar_pdf(str(pdf))
                        
                        if sucesso:
                            adicionar_log(f"✅ {pdf.name} processado", "success")
                        else:
                            adicionar_log(f"❌ Erro em {pdf.name}", "error")
                        
                        progress_bar.progress((i + 1) / len(pdfs))
                    
                    status_text.text("Processamento concluído!")
                    st.success(f"✅ {len(pdfs)} PDFs processados!")
                    st.balloons()
        
        with col2:
            st.subheader("Upload de PDF")
            
            uploaded_file = st.file_uploader(
                "Fazer upload de PDF",
                type=['pdf'],
                help="Faça upload de um PDF para processar imediatamente"
            )
            
            if uploaded_file is not None:
                # Salvar arquivo na pasta de entrada
                pasta = Path(pasta_entrada)
                caminho_temp = pasta / uploaded_file.name
                
                with open(caminho_temp, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"Arquivo salvo: {uploaded_file.name}")
                
                if st.button("Processar Agora"):
                    with st.spinner("Processando..."):
                        sucesso, dados = st.session_state.processador.processar_pdf(str(caminho_temp))
                        
                        if sucesso:
                            st.success("✅ Processamento concluído!")
                            st.json(dados)
                        else:
                            st.error("❌ Erro no processamento")
                            if dados:
                                st.json(dados)
    
    # Tab 3 - Estatísticas
    with tab3:
        st.header("Estatísticas Detalhadas")
        
        # Tentar obter estatísticas do Excel
        if usar_excel:
            try:
                writer = WriterExcel(arquivo_excel)
                stats_excel = writer.obter_estatisticas()
                
                if stats_excel:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Resumo Geral")
                        st.metric("Total de Faturas", stats_excel.get('total_faturas', 0))
                        st.metric("Clientes Únicos", stats_excel.get('clientes_unicos', 0))
                        st.metric("UCs Únicas", stats_excel.get('ucs_unicas', 0))
                    
                    with col2:
                        st.subheader("💰 Valores")
                        st.metric(
                            "Valor Total", 
                            f"R$ {stats_excel.get('valor_total_soma', 0):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                        )
                        st.metric(
                            "Valor Médio", 
                            f"R$ {stats_excel.get('valor_medio', 0):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                        )
                        st.metric("Consumo Médio", f"{stats_excel.get('consumo_medio', 0):.2f} kWh")
                    
                    # Mostrar últimas faturas
                    st.subheader("📋 Últimas Faturas Processadas")
                    
                    df = pd.read_excel(arquivo_excel)
                    if len(df) > 0:
                        st.dataframe(df.tail(10), use_container_width=True)
                    else:
                        st.info("Nenhuma fatura processada ainda")
                else:
                    st.info("Nenhuma fatura processada ainda")
                    
            except Exception as e:
                st.warning(f"Não foi possível carregar estatísticas: {str(e)}")
        else:
            st.info("Ative o Excel nas configurações para ver estatísticas")
    
    # Tab 4 - Logs
    with tab4:
        st.header("Logs do Sistema")
        
        # Mostrar logs da sessão
        if st.session_state.logs:
            for log in st.session_state.logs:
                if log['tipo'] == 'success':
                    st.success(f"[{log['timestamp']}] {log['mensagem']}")
                elif log['tipo'] == 'error':
                    st.error(f"[{log['timestamp']}] {log['mensagem']}")
                else:
                    st.info(f"[{log['timestamp']}] {log['mensagem']}")
        else:
            st.info("Nenhum log disponível")
        
        st.divider()
        
        # Mostrar arquivo de log
        st.subheader("📄 Arquivo de Log")
        
        log_file = Path('logs/processamento.log')
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            # Mostrar últimas 50 linhas
            st.text_area(
                "Últimas entradas do log",
                value=''.join(logs[-50:]),
                height=400
            )
        else:
            st.info("Arquivo de log ainda não criado")
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>RPA COELBA - Sistema de Leitura Automatizada de Faturas de Energia</p>
            <p>Desenvolvido com Python, Streamlit e IA</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
