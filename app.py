import streamlit as st
import sqlite3
import pandas as pd

# 1. Conexão com o Banco (Isso deve vir primeiro)
conn = sqlite3.connect('vendas.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT,
        quantidade INTEGER
    )
''')
conn.commit()

# 2. Título e Visual
st.title("✒️ Loja da Caneta Premium")
st.write("Bem-vindo à nossa loja experimental!")

# 3. As Caixas de Texto (Onde o usuário interage)
# IMPORTANTE: Verifique se estas linhas abaixo existem no seu arquivo:
nome = st.text_input("Digite seu nome completo:")
quantidade = st.number_input("Quantas canetas você deseja?", min_value=1, max_value=10)

if st.button("Finalizar Compra"):
    if nome:
        c.execute('INSERT INTO pedidos (nome_cliente, quantidade) VALUES (?, ?)', (nome, quantidade))
        conn.commit()
        st.success(f"Pedido de {nome} enviado com sucesso!")
        st.balloons()
    else:
        st.warning("Por favor, digite seu nome antes de comprar.")

# --- DIVISÃO DO SITE EM ABAS ---
aba_loja, aba_admin = st.tabs(["🛒 Comprar Caneta", "🔐 Área do Dono"])

with aba_loja:
    st.subheader("Faça seu pedido")
    # Mova os campos de nome e quantidade para cá se quiser organizar melhor
    st.write("Escolha sua caneta premium e finalize a compra abaixo.")

with aba_admin:
    st.subheader("Acesso Restrito")
    senha = st.text_input("Digite a senha para ver as vendas:", type="password")
    
    if senha == "bruno123": # Você pode escolher a senha que quiser
        st.success("Acesso liberado, Bruno!")
        df = pd.read_sql_query("SELECT * FROM pedidos", conn)
        st.table(df)
        
        # Botão extra: Exportar para CSV (útil para o seu controle)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar Relatório em Excel/CSV", csv, "vendas.csv", "text/csv")
    elif senha != "":
        st.error("Senha incorreta!")