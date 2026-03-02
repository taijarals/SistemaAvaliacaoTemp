import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def tela_usuarios():

    st.title("👥 Gerenciamento de Usuários")

    # Buscar todos perfis
    response = supabase.table("perfis").select("*").execute()

    if not response.data:
        st.info("Nenhum usuário encontrado.")
        return

    usuarios = response.data

    nomes = [u["nome_completo"] for u in usuarios]

    usuario_selecionado = st.selectbox(
        "Selecione um usuário",
        nomes,
        key="usuarios_select"
    )

    usuario = next(u for u in usuarios if u["nome_completo"] == usuario_selecionado)

    st.divider()

    st.subheader("📄 Dados do Usuário")

    st.write(f"ID: {usuario['id']}")
    st.write(f"Nome: {usuario['nome_completo']}")
    st.write(f"Curso: {usuario['curso']}")
    st.write(f"Tipo: {usuario['tipo_usuario']}")

    st.divider()

    # ==========================
    # ALTERAR CURSO
    # ==========================
    novo_curso = st.text_input(
        "Alterar curso",
        value=usuario["curso"],
        key="usuarios_curso"
    )

    if st.button("💾 Atualizar Curso", key="usuarios_update"):
        supabase.table("perfis") \
            .update({"curso": novo_curso}) \
            .eq("id", usuario["id"]) \
            .execute()

        st.success("Curso atualizado!")
        st.rerun()

    st.divider()

    # ==========================
    # ALTERAR PRIVILÉGIO
    # ==========================
    if usuario["tipo_usuario"] == "admin":

        if st.button("⬇️ Remover Admin", key="usuarios_remove_admin"):
            supabase.table("perfis") \
                .update({"tipo_usuario": "aluno"}) \
                .eq("id", usuario["id"]) \
                .execute()

            st.success("Privilégio removido!")
            st.rerun()

    else:

        if st.button("⬆️ Tornar Admin", key="usuarios_make_admin"):
            supabase.table("perfis") \
                .update({"tipo_usuario": "admin"}) \
                .eq("id", usuario["id"]) \
                .execute()

            st.success("Usuário promovido a admin!")
            st.rerun()

    st.divider()

    # ==========================
    # DELETAR USUÁRIO
    # ==========================
    st.warning("⚠️ Zona perigosa")

    if st.button("🗑️ Deletar Usuário", key="usuarios_delete"):

        # Deleta apenas da tabela perfis
        supabase.table("perfis") \
            .delete() \
            .eq("id", usuario["id"]) \
            .execute()

        st.success("Usuário removido da tabela perfis.")
        st.rerun()