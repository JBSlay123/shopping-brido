import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    # Tenta carregar o arquivo CSV
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    # Cria um novo DataFrame se o arquivo não existir
    dados = pd.DataFrame({"produtos": [], "preços": []})
    dados.to_csv("compras.csv", index=False)

st.title("Controle de Compras")

# Recebe o orçamento do usuário
orçamento = st.number_input("Orçamento", min_value=0.0)

# Calcula o total de gastos atuais
total = dados["preços"].sum() if not dados.empty else 0

# Exibe o total de gastos e o restante do orçamento
st.write(f"Total gasto: R${total:.2f}")
st.write(f"Orçamento restante: R${(orçamento - total):.2f}")

# Formulário para adicionar itens
with st.form("Adicione item"):
    produto = st.text_input("Adicione Produto:")
    preço = st.number_input("Adicione Preço:", min_value=0.0)
    submit = st.form_submit_button("Adicionar")

    if submit:
        if preço <= (orçamento - total):
            # Adiciona o novo produto e preço ao DataFrame
            novo_produto = pd.DataFrame({"produtos": [produto], "preços": [preço]})
            dados = pd.concat([dados, novo_produto], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada com sucesso!")
        else:
            st.error("Sem orçamento suficiente.")

# Exibe os dados da tabela de compras
st.subheader("Lista de Compras")
st.dataframe(dados)
