import streamlit as st
from supabase import create_client
from pages.login import tela_login
from pages.votacao import tela_votacao
from pages.admin import tela_admin
from pages.disciplinas import tela_disciplinas
from pages.desafios import tela_desafios
from pages.usuarios import tela_usuarios
from pages.cursos import tela_cursos
from services.supabase_client import supabase

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
#SUPABASE_URL = st.secrets["SUPABASE_URL"]
#SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
#supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔐 Só define sessão se existir
if "session" in st.session_state:
    supabase.auth.set_session(
        st.session_state.session.access_token,
        st.session_state.session.refresh_token
    )


# =========================================================
# 4️⃣ BUSCAR PERFIL (apenas uma vez por sessão)
# =========================================================
if "perfil" not in st.session_state:

    response = supabase.table("perfis") \
        .select("*") \
        .eq("id", st.session_state.user.id) \
        .execute()

    if not response.data:
        st.error("Perfil não encontrado.")
        st.stop()

    perfil = response.data[0]

    # Salva tudo globalmente
    st.session_state.perfil = perfil
    st.session_state.tipo_usuario = perfil["tipo_usuario"]
    st.session_state.nome_usuario = perfil["nome_completo"]

# Agora pode usar em qualquer página:
tipo_usuario = st.session_state.tipo_usuario
nome_usuario = st.session_state.nome_usuario


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

    # Primeira linha de botões
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗳️ Votação", width="stretch"):
            st.session_state.pagina = "votacao"
            st.rerun()

    with col2:
        if st.button("👥 Gerenciar Usuários", width="stretch"):
            st.session_state.pagina = "usuarios"
            st.rerun()

    # Área exclusiva de admin
    if tipo_usuario == "admin":

        st.divider()
        st.subheader("Área Administrativa")

        col3, col4 = st.columns(2)

        with col3:
            if st.button("🏫 Universidades", width="stretch"):
                st.session_state.pagina = "admin"
                st.rerun()

        with col4:
            if st.button("🗂️ Disciplinas", width="stretch"):
                st.session_state.pagina = "disciplinas"
                st.rerun()

        col5, col6 = st.columns(2)

        with col5:
            if st.button("🎯 Desafios", width="stretch"):
                st.session_state.pagina = "desafios"
                st.rerun()

        with col6:
            if st.button("📚 Cursos", width="stretch"):
                st.session_state.pagina = "cursos"
                st.rerun()

# =========================================================
# 7️⃣ ROTAS
# =========================================================
elif st.session_state.pagina == "votacao":
    tela_votacao()

elif st.session_state.pagina == "universidades" and tipo_usuario == "admin":
    tela_universidades()

elif st.session_state.pagina == "disciplinas" and tipo_usuario == "admin":
    tela_disciplinas()

elif st.session_state.pagina == "cursos" and tipo_usuario == "admin":
    tela_cursos()

elif st.session_state.pagina == "desafios" and tipo_usuario == "admin":
    tela_desafios()

elif st.session_state.pagina == "usuarios":
    tela_usuarios()

else:
    st.warning("Você não tem permissão para acessar esta página.")
    st.session_state.pagina = "inicio"
    st.rerun()