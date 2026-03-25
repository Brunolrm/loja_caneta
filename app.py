import streamlit as st
import sqlite3
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Caneta Premium Executiva", layout="wide")

# Conexão com o banco (Mantendo sua estrutura)
conn = sqlite3.connect('vendas.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_cliente TEXT, quantidade INTEGER, data TEXT)')
conn.commit()

# --- ESTILO CSS PERSONALIZADO (Para dar o ar profissional) ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; background-color: #1f77b4; color: white; }
    .preco { font-size: 24px; color: #2e7d32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("✒️ Exclusive Pen Store")
st.write("---")

# --- ORGANIZAÇÃO EM ABAS ---
tab_loja, tab_admin = st.tabs(["🛒 Vitrine de Vendas", "🔐 Gestão de Negócio"])

with tab_loja:
    # Divisão em duas colunas: Imagem vs. Compra
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        st.image("https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800", 
                 caption="Caneta Tinteiro Série Ouro - Edição Limitada")
        
    with col_info:
        st.header("Caneta Tinteiro Premium")
        st.markdown("<p class='preco'>R$ 45,90</p>", unsafe_allow_html=True)
        st.write("""
        A ferramenta definitiva para quem valoriza a escrita. 
        - Corpo em fibra de carbono
        - Ponta de irídio alemã
        - Design ergonômico
        """)
        
        st.divider()
        
        # Formulário de Compra
        nome = st.text_input("Nome do Comprador")
        qtd = st.select_slider("Quantidade", options=[1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,20,30,50,100])
        
        if st.button("FINALIZAR PEDIDO"):
            if nome:
                import datetime
                data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                c.execute('INSERT INTO pedidos (nome_cliente, quantidade, data) VALUES (?, ?, ?)', (nome, qtd, data_atual))
                conn.commit()
                st.success(f"Excelente escolha, {nome}! Pedido processado.")
                st.balloons()
            else:
                st.error("Por favor, informe seu nome para o envio.")

with tab_admin:
    st.header("Painel Administrativo")
    senha = st.text_input("Chave de Acesso", type="password")
    
    if senha == "bruno123":
        # MÉTRICAS TOTAIS (O segredo do visual profissional)
        df = pd.read_sql_query("SELECT * FROM pedidos", conn)
        total_vendas = df['quantidade'].sum() if not df.empty else 0
        faturamento = total_vendas * 45.90
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Unidades Vendidas", f"{total_vendas} un")
        c2.metric("Faturamento Total", f"R$ {faturamento:,.2f}")
        c3.metric("Ticket Médio", f"R$ {45.90:,.2f}")
        
        st.write("---")
        st.subheader("Lista de Pedidos Recentes")
        st.dataframe(df, use_container_width=True)
    elif senha:
        st.warning("Acesso negado.")