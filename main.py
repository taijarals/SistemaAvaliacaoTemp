import streamlit as st
from pages.votacao import tela_votacao
from pages.admin import tela_admin

st.set_page_config(page_title="Sistema de Avaliação", layout="centered")

# ----------------------------
# CONTROLE DE NAVEGAÇÃO
# ----------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# ----------------------------
# TELA INICIAL
# ----------------------------
if st.session_state.pagina == "inicio":

    st.title("Sistema de Avaliação")

    st.write("Selecione uma opção:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗳️ Votação", use_container_width=True):
            st.session_state.pagina = "votacao"
            st.rerun()

    with col2:
        if st.button("🔒 Painel Administrativo", use_container_width=True):
            st.session_state.pagina = "admin"
            st.rerun()

# ----------------------------
# TELA DE VOTAÇÃO
# ----------------------------
elif st.session_state.pagina == "votacao":

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "inicio"
        st.rerun()

    tela_votacao()

# ----------------------------
# TELA ADMIN
# ----------------------------
elif st.session_state.pagina == "admin":

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "inicio"
        st.rerun()

    tela_admin()