import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def tela_usuarios():

    st.title("👥 Gerenciamento de Usuários")

    # Buscar perfis
    response = supabase.table("perfis").select("*").execute()

    if not response.data:
        st.info("Nenhum usuário encontrado.")
        return

    usuarios = response.data

    nomes = [u["nome_completo"] for u in usuarios]

    usuario_selecionado = st.selectbox(
        "Selecione um usuário",
        nomes,
        key="usuarios_select",
        disabled=(st.session_state.tipo_usuario != "admin")
    )

    usuario = next(u for u in usuarios if u["nome_completo"] == usuario_selecionado)

    st.divider()

    # ==========================
    # DADOS DO USUÁRIO
    # ==========================
    st.subheader("📄 Dados do Usuário")

    st.write(f"ID: {usuario['id']}")
    st.write(f"Nome: {usuario['nome_completo']}")
    st.write(f"Curso: {usuario.get('curso', 'Não informado')}")
    st.write(f"Tipo: {usuario['tipo_usuario']}")

    st.divider()

    # ==========================
    # ALTERAÇÕES
    # ==========================
    st.subheader("✏️ Alterar Dados")

    novo_nome = st.text_input(
        "Nome completo",
        value=usuario["nome_completo"],
        key="usuarios_nome"
    )

    # Lista fixa de cursos (você pode depois buscar do banco)
    cursos_disponiveis = [
        "Engenharia da Computação",
        "Ciência da Computação",
        "Sistemas de Informação",
        "Engenharia de Software",
        "Outro"
    ]

    novo_curso = st.selectbox(
        "Curso",
        cursos_disponiveis,
        index=cursos_disponiveis.index(usuario["curso"])
        if usuario["curso"] in cursos_disponiveis else 0,
        key="usuarios_curso"
    )

    novo_tipo = st.selectbox(
        "Tipo de usuário",
        ["aluno", "admin"],
        index=0 if usuario["tipo_usuario"] == "aluno" else 1,
        key="usuarios_tipo",
        disabled=(st.session_state.tipo_usuario != "admin")
    )

    if st.button("💾 Salvar Alterações", key="usuarios_update"):

        supabase.table("perfis") \
            .update({
                "nome_completo": novo_nome,
                "curso": novo_curso,
                "tipo_usuario": novo_tipo
            }) \
            .eq("id", usuario["id"]) \
            .execute()

        st.success("Usuário atualizado com sucesso!")
        st.rerun()

    st.divider()

    # ==========================
    # ZONA PERIGOSA
    # ==========================
    #st.warning("⚠️ Zona perigosa")

    if st.button("🗑️ Deletar Usuário", key="usuarios_delete"):

        supabase.table("perfis") \
            .delete() \
            .eq("id", usuario["id"]) \
            .execute()

        st.success("Usuário removido da tabela perfis.")
        st.rerun()