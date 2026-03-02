import streamlit as st
import pandas as pd
from services.supabase_client import supabase

def tela_disciplinas():

    st.subheader("Gerenciar Disciplinas")

    nome = st.text_input("Nome da Disciplina")
    curso = st.text_input("Nome do Curso")
    dia = st.text_input("Dia da Aula")

    if st.button("Cadastrar Disciplina"):
        supabase.table("disciplinas").insert({
            "nome_disciplina": nome,
            "nome_curso": curso,
            "dia_aula": dia
        }).execute()
        st.success("Disciplina cadastrada!")
        st.rerun()

    st.divider()

    response = supabase.table("disciplinas").select("*").execute()

    if response.data:
        df = pd.DataFrame(response.data)
        st.dataframe(df)

        disciplina_id = st.selectbox(
            "Selecione ID para excluir",
            df["id"]
        )

        if st.button("Excluir Disciplina"):
            supabase.table("disciplinas").delete().eq("id", disciplina_id).execute()
            st.success("Disciplina excluída!")
            st.rerun()