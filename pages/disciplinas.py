import streamlit as st
import pandas as pd
from services.supabase_client import supabase


def tela_disciplinas():

    st.subheader("📚 Gerenciar Disciplinas")

    # ==========================
    # BUSCAR CURSOS
    # ==========================

    response_cursos = supabase.table("cursos").select("*").order("nome_curso").execute()

    if not response_cursos.data:
        st.warning("Cadastre um curso antes de criar disciplinas.")
        return

    cursos = response_cursos.data
    nomes_cursos = [c["nome_curso"] for c in cursos]

    # ==========================
    # CADASTRO
    # ==========================

    st.subheader("➕ Cadastrar Disciplina")

    nome_disciplina = st.text_input("Nome da Disciplina")
    curso_selecionado = st.selectbox("Curso", nomes_cursos)
    dia_aula = st.text_input("Dia da Aula")

    if st.button("Cadastrar Disciplina"):

        if not nome_disciplina.strip():
            st.warning("Informe o nome da disciplina.")
            return

        curso_id = next(
            c["id"] for c in cursos if c["nome_curso"] == curso_selecionado
        )

        response = supabase.table("disciplinas").insert({
            "nome_disciplina": nome_disciplina,
            "curso_id": curso_id,
            "dia_aula": dia_aula
        }).execute()

        if response.data:
            st.success("Disciplina cadastrada!")
            st.rerun()
        else:
            st.error("Erro ao cadastrar disciplina.")

    st.divider()

    # ==========================
    # LISTAGEM COM JOIN
    # ==========================

    st.subheader("📋 Disciplinas Cadastradas")

    response = supabase.table("disciplinas") \
        .select("id, nome_disciplina, dia_aula, cursos(nome_curso)") \
        .order("id") \
        .execute()

    if response.data:

        dados = []
        for d in response.data:
            dados.append({
                "ID": d["id"],
                "Disciplina": d["nome_disciplina"],
                "Curso": d["cursos"]["nome_curso"] if d["cursos"] else "—",
                "Dia": d["dia_aula"]
            })

        df = pd.DataFrame(dados)

        st.dataframe(df, use_container_width=True)

        st.divider()

        # ==========================
        # ALTERAÇÃO
        # ==========================

        st.subheader("✏️ Alterar Disciplina")

        disciplina_id_edit = st.selectbox(
            "Selecione a disciplina",
            df["ID"],
            key="disciplina_edit_select"
        )

        disciplina_atual = next(
            d for d in response.data if d["id"] == disciplina_id_edit
        )

        nome_edit = st.text_input(
            "Nome da Disciplina",
            value=disciplina_atual["nome_disciplina"],
            key="edit_nome"
        )

        curso_edit = st.selectbox(
            "Curso",
            nomes_cursos,
            index=nomes_cursos.index(
                disciplina_atual["cursos"]["nome_curso"]
            ) if disciplina_atual["cursos"] else 0,
            key="edit_curso"
        )

        dia_edit = st.text_input(
            "Dia da Aula",
            value=disciplina_atual["dia_aula"],
            key="edit_dia"
        )

        if st.button("Salvar Alterações"):

            curso_id = next(
                c["id"] for c in cursos if c["nome_curso"] == curso_edit
            )

            supabase.table("disciplinas") \
                .update({
                    "nome_disciplina": nome_edit,
                    "curso_id": curso_id,
                    "dia_aula": dia_edit
                }) \
                .eq("id", disciplina_id_edit) \
                .execute()

            st.success("Disciplina atualizada!")
            st.rerun()

        st.divider()

        # ==========================
        # EXCLUSÃO
        # ==========================

        st.subheader("🗑️ Excluir Disciplina")

        disciplina_id = st.selectbox(
            "Selecione a disciplina para excluir",
            df["ID"],
            key="disciplina_delete_select"
        )

        if st.button("Excluir Disciplina"):

            supabase.table("disciplinas") \
                .delete() \
                .eq("id", disciplina_id) \
                .execute()

            st.success("Disciplina excluída!")
            st.rerun()

    else:
        st.info("Nenhuma disciplina cadastrada.")