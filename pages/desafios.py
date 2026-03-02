import streamlit as st
from supabase import create_client
import os

# conexão
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


def tela_desafios():

    st.title("Cadastro de Desafios")

    # ----------------------------
    # CARREGAR DISCIPLINAS
    # ----------------------------
    disciplinas = supabase.table("disciplinas").select("*").execute().data

    if not disciplinas:
        st.warning("Cadastre uma disciplina antes de criar desafios.")
        return

    disciplina_dict = {d["nome_disciplina"]: d["id"] for d in disciplinas}

    # ----------------------------
    # FORMULÁRIO
    # ----------------------------
    with st.form("form_desafio"):

        titulo = st.text_input("Título do Desafio")
        descricao = st.text_area("Descrição")
        disciplina_nome = st.selectbox(
            "Disciplina",
            list(disciplina_dict.keys())
        )

        submitted = st.form_submit_button("Salvar")

        if submitted:
            if titulo.strip() == "":
                st.error("Título é obrigatório")
            else:
                supabase.table("desafios").insert({
                    "titulo": titulo,
                    "descricao": descricao,
                    "fk_disciplina": disciplina_dict[disciplina_nome]
                }).execute()

                st.success("Desafio cadastrado com sucesso!")
                st.rerun()

    # ----------------------------
    # LISTAGEM
    # ----------------------------
    st.subheader("Desafios Cadastrados")

    desafios = supabase.table("desafios") \
        .select("id, titulo, descricao, ativo, disciplinas(nome_disciplina)") \
        .execute().data

    if desafios:

        for d in desafios:
            with st.container():
                st.markdown(f"### {d['titulo']}")
                st.write(f"Disciplina: {d['disciplinas']['nome_disciplina']}")
                st.write(d["descricao"])
                st.write(f"Ativo: {'Sim' if d['ativo'] else 'Não'}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Desativar {d['id']}"):
                        supabase.table("desafios") \
                            .update({"ativo": False}) \
                            .eq("id", d["id"]) \
                            .execute()
                        st.rerun()

                with col2:
                    if st.button(f"Excluir {d['id']}"):
                        supabase.table("desafios") \
                            .delete() \
                            .eq("id", d["id"]) \
                            .execute()
                        st.rerun()

                st.divider()
    else:
        st.info("Nenhum desafio cadastrado.")