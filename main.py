import streamlit as st
from supabase import create_client
from pages.login import tela_login
from pages.votacao import tela_votacao
from pages.admin import tela_admin
from pages.disciplinas import tela_disciplinas
from pages.desafios import tela_desafios
from pages.usuarios import tela_usuarios

st.set_page_config(page_title="Sistema de Avaliação", layout="centered")

# =========================================================
# 1️⃣ CONTROLE DE ESTADO INICIAL
# =========================================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"


# =========================================================
# 2️⃣ CONTROLE DE LOGIN
# =========================================================
if "user" not in st.session_state:
    tela_login()
    st.stop()


# =========================================================
# 3️⃣ CONEXÃO SUPABASE
# =========================================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================================================
# 4️⃣ BUSCAR PERFIL (apenas uma vez por sessão)
# =========================================================
if "perfil" not in st.session_state:
    perfil = supabase.table("perfis") \
        .select("*") \
        .eq("id", st.session_state.user.id) \
        .execute()

    if not perfil.data:
        st.error("Perfil não encontrado.")
        st.stop()

    st.session_state.perfil = perfil.data[0]

perfil = st.session_state.perfil
tipo_usuario = perfil["tipo_usuario"]
nome_usuario = perfil["nome_completo"]


# =========================================================
# 5️⃣ HEADER
# =========================================================
col1, col2 = st.columns([4, 1])

with col1:
    st.write(f"👤 Usuário: {nome_usuario}")

with col2:
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


st.divider()


# =========================================================
# BOTÃO VOLTAR GLOBAL
# =========================================================
if st.session_state.pagina != "inicio":
    if st.button("⬅️ Voltar", key="btn_voltar_global"):
        st.session_state.pagina = "inicio"
        st.rerun()

    st.divider()

# =========================================================
# 6️⃣ TELA INICIAL
# =========================================================
if st.session_state.pagina == "inicio":

    st.title("Sistema de Avaliação")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗳️ Votação", use_container_width=True):
            st.session_state.pagina = "votacao"
            st.rerun()
    
    with st.button("👥 Gerenciar Usuários", use_container_width=True):
    st.session_state.pagina = "usuarios"
    st.rerun()

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


# =========================================================
# 7️⃣ ROTAS
# =========================================================
elif st.session_state.pagina == "votacao":
    tela_votacao()

elif st.session_state.pagina == "admin" and tipo_usuario == "admin":
    tela_admin()

elif st.session_state.pagina == "disciplinas" and tipo_usuario == "admin":
    tela_disciplinas()

elif st.session_state.pagina == "desafios" and tipo_usuario == "admin":
    tela_desafios()

else:
    st.warning("Você não tem permissão para acessar esta página.")
    st.session_state.pagina = "inicio"
    st.rerun()

elif st.session_state.pagina == "usuarios" and tipo_usuario == "admin":
    tela_usuarios()