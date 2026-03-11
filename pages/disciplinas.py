import streamlit as st
import pandas as pd
from services.supabase_client import supabase


def tela_disciplinas():

    st.subheader("📚 Gerenciar Disciplinas")

    # ==========================
    # BUSCAR CURSOS
    # ==========================

    response_cursos = supabase.table("cursos").select("*").order("nome_curso").execute()
    cursos = response_cursos.data

    cursos_dict = {c["id"]: c["nome_curso"] for c in cursos}
    cursos_dict_rev = {v: k for k, v in cursos_dict.items()}

    # ==========================
    # BUSCAR DISCIPLINAS
    # ==========================

    response = supabase.table("disciplinas") \
        .select("id, nome_disciplina, dia_aula, cursos(nome_curso)") \
        .order("id") \
        .execute()

    if not response.data:
        st.info("Nenhuma disciplina cadastrada.")
        return

    dados = []

    for d in response.data:
        dados.append({
            "id": d["id"],
            "Disciplina": d["nome_disciplina"],
            "Curso": d["cursos"]["nome_curso"] if d["cursos"] else "",
            "Dia": d["dia_aula"]
        })

    df = pd.DataFrame(dados)

    st.write("### ✏️ Edite diretamente na tabela")

    df_editado = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    # ==========================
    # BOTÃO SALVAR
    # ==========================

    if st.button("💾 Salvar Alterações"):

        for _, row in df_editado.iterrows():

            curso_id = cursos_dict_rev.get(row["Curso"])

            supabase.table("disciplinas") \
                .update({
                    "nome_disciplina": row["Disciplina"],
                    "dia_aula": row["Dia"],
                    "curso_id": curso_id
                }) \
                .eq("id", row["id"]) \
                .execute()

        st.success("Alterações salvas!")
        st.rerun()

    # ==========================
    # EXCLUSÃO
    # ==========================

    st.divider()

    disciplina_delete = st.selectbox(
        "Selecione disciplina para excluir",
        df["id"]
    )

    if st.button("🗑️ Excluir Disciplina"):

        supabase.table("disciplinas") \
            .delete() \
            .eq("id", disciplina_delete) \
            .execute()

        st.success("Disciplina excluída!")
        st.rerun()