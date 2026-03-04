import streamlit as st
import pandas as pd
from services.supabase_client import supabase
from pages.disciplinas import tela_disciplinas

def tela_admin():

    aba = st.selectbox(
        "Seção",
        ["Disciplinas", "Relatórios"],
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