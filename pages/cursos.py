import streamlit as st
import pandas as pd
from services.supabase_client import supabase


def tela_cursos():

    st.subheader("🎓 Gerenciar Cursos")

    # ==========================
    # CADASTRO
    # ==========================

    nome_curso = st.text_input("Nome do Curso")

    if st.button("Cadastrar Curso"):

        if nome_curso.strip() == "":
            st.warning("Informe um nome válido.")
            return

        response = supabase.table("cursos").insert({
            "nome_curso": nome_curso
        }).execute()

        if response.data:
            st.success("Curso cadastrado!")
            st.rerun()
        else:
            st.error("Erro ao cadastrar curso.")

    st.divider()

    # ==========================
    # LISTAGEM
    # ==========================

    response = supabase.table("cursos").select("*").order("id").execute()

    if response.data:

        df = pd.DataFrame(response.data)
        st.dataframe(df, use_container_width=True)

        st.divider()

        # ==========================
        # EXCLUSÃO
        # ==========================

        curso_id = st.selectbox(
            "Selecione o curso para excluir",
            df["id"],
            key="curso_delete_select"
        )

        if st.button("Excluir Curso"):

            supabase.table("cursos") \
                .delete() \
                .eq("id", curso_id) \
                .execute()

            st.success("Curso excluído!")
            st.rerun()

    else:
        st.info("Nenhum curso cadastrado.")