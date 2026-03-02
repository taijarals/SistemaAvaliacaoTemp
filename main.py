import streamlit as st
from pages.login import tela_login
from pages.votacao import tela_votacao
from pages.admin import tela_admin
from pages.disciplinas import tela_disciplinas
from pages.desafios import tela_desafios

st.set_page_config(page_title="Sistema de Avaliação", layout="centered")

# ----------------------------
# CONTROLE DE LOGIN
# ----------------------------
if "user" not in st.session_state:
    tela_login()
    st.stop()

# ----------------------------
# CONTROLE DE NAVEGAÇÃO
# ----------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# Buscar tipo do usuário
from supabase import create_client
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

perfil = supabase.table("perfis").select("*") \
    .eq("id", st.session_state.user.id) \
    .execute()

tipo_usuario = perfil.data[0]["tipo_usuario"]

# ----------------------------
# HEADER
# ----------------------------
col1, col2 = st.columns([4,1])
with col1:
    st.write(f"Usuário: {perfil.data[0]['nome_completo']}")
with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ----------------------------
# TELA INICIAL
# ----------------------------
if st.session_state.pagina == "inicio":

    st.title("Sistema de Avaliação")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗳️ Votação", use_container_width=True):
            st.session_state.pagina = "votacao"
            st.rerun()

    # Apenas admin pode ver painel
    if tipo_usuario == "admin":

        with col2:
            if st.button("🔒 Painel Administrativo", use_container_width=True):
                st.session_state.pagina = "admin"
                st.rerun()

        col3, col4 = st.columns(2)

        with col3:
            if st.button("📚 Disciplinas", use_container_width=True):
                st.session_state.pagina = "disciplinas"
                st.rerun()

        with col4:
            if st.button("🎯 Desafios", use_container_width=True):
                st.session_state.pagina = "desafios"
                st.rerun()

# ----------------------------
# ROTAS
# ----------------------------
elif st.session_state.pagina == "votacao":
    tela_votacao()

elif st.session_state.pagina == "admin" and tipo_usuario == "admin":
    tela_admin()

elif st.session_state.pagina == "disciplinas" and tipo_usuario == "admin":
    tela_disciplinas()

elif st.session_state.pagina == "desafios" and tipo_usuario == "admin":
    tela_desafios()