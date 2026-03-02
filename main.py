import streamlit as st
from pages.votacao import tela_votacao
from pages.admin import tela_admin
from pages.disciplinas import tela_disciplinas
from pages.desafios import tela_desafios

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
    col3, col4 = st.columns(2)

    with col1:
        if st.button("🗳️ Votação", use_container_width=True):
            st.session_state.pagina = "votacao"
            st.rerun()

    with col2:
        if st.button("🔒 Painel Administrativo", use_container_width=True):
            st.session_state.pagina = "admin"
            st.rerun()

    with col3:
        if st.button("📚 Cadastro de Disciplinas", use_container_width=True):
            st.session_state.pagina = "disciplinas"
            st.rerun()

    with col4:
        if st.button("🎯 Cadastro de Desafios", use_container_width=True):
            st.session_state.pagina = "desafios"
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


# ----------------------------
# TELA DISCIPLINAS
# ----------------------------
elif st.session_state.pagina == "disciplinas":

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "inicio"
        st.rerun()

    tela_disciplinas()


# ----------------------------
# TELA DESAFIOS
# ----------------------------
elif st.session_state.pagina == "desafios":

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "inicio"
        st.rerun()

    tela_desafios()