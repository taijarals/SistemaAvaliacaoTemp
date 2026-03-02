import streamlit as st
import pandas as pd
from services.supabase_client import supabase
from pages.disciplinas import tela_disciplinas

def tela_admin():

    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = False

    if not st.session_state.admin_logado:
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if senha == ADMIN_PASSWORD:
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
        return

    aba = st.selectbox(
        "Seção",
        ["Disciplinas", "Relatórios"]
        key="admin_selectbox"
    )

    if aba == "Disciplinas":
        tela_disciplinas()

    elif aba == "Relatórios":
        response = supabase.table("votos").select("*").execute()

        if response.data:
            df = pd.DataFrame(response.data)

            medias = (
                df.groupby("disciplina")["media"]
                .mean()
                .reset_index()
                .sort_values(by="media", ascending=False)
            )

            medias["media"] = medias["media"].round(3)
            medias["posição"] = range(1, len(medias) + 1)

            st.dataframe(medias)
        else:
            st.info("Nenhum voto ainda.")