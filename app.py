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

# 4. Visualizar o Banco de Dados (Para você testar)
st.divider()
st.subheader("📦 Registro Interno de Vendas")
df = pd.read_sql_query("SELECT * FROM pedidos", conn)
st.table(df)