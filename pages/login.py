import streamlit as st
from supabase import create_client
import os

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def tela_login():

    st.title("🔐 Login")

    aba = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    # =========================
    # LOGIN
    # =========================
    if aba == "Login":

        if st.button("Entrar"):

            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": senha
                })

                st.session_state.user = response.user
                st.session_state.session = response.session

                st.success("Login realizado com sucesso!")
                st.rerun()

            except Exception:
                st.error("Email ou senha inválidos")

    # =========================
    # CADASTRO
    # =========================
    else:

        nome = st.text_input("Nome Completo")
        curso = st.selectbox("Curso", [
            "Engenharia da Computação",
            "Ciência da Computação",
            "Sistemas de Informação"
        ])

        if st.button("Cadastrar"):

            try:
                response = supabase.auth.sign_up({
                    "email": email,
                    "password": senha
                })

                user_id = response.user.id

                supabase.table("perfis").insert({
                    "id": user_id,
                    "nome_completo": nome,
                    "curso": curso,
                    "tipo_usuario": "aluno"
                }).execute()

                st.success("Cadastro realizado! Faça login.")

            except Exception as e:
                st.error(f"Erro no cadastro: {e}")