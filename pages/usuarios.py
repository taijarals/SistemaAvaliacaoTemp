import streamlit as st
from supabase import create_client

def tela_usuarios():

    st.title("👥 Gerenciar Usuários")

    # Conexão
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    # Botão voltar
    if st.button("⬅ Voltar"):
        st.session_state.pagina = "inicio"
        st.rerun()

    st.divider()

    # Buscar usuários
    usuarios = supabase.table("perfis").select("*").execute()

    if not usuarios.data:
        st.warning("Nenhum usuário encontrado.")
        return

    for user in usuarios.data:

        with st.expander(f"{user['nome_completo']} ({user['tipo_usuario']})"):

            # Campos editáveis
            novo_nome = st.text_input(
                "Nome Completo",
                value=user["nome_completo"],
                key=f"nome_{user['id']}"
            )

            novo_curso = st.text_input(
                "Curso",
                value=user.get("curso", ""),
                key=f"curso_{user['id']}"
            )

            novo_tipo = st.selectbox(
                "Tipo de Usuário",
                ["aluno", "admin"],
                index=0 if user["tipo_usuario"] == "aluno" else 1,
                key=f"tipo_{user['id']}"
            )

            col1, col2 = st.columns(2)

            # Salvar alterações
            with col1:
                if st.button("💾 Salvar Alterações", key=f"salvar_{user['id']}"):

                    supabase.table("perfis") \
                        .update({
                            "nome_completo": novo_nome,
                            "curso": novo_curso,
                            "tipo_usuario": novo_tipo
                        }) \
                        .eq("id", user["id"]) \
                        .execute()

                    st.success("Usuário atualizado com sucesso!")
                    st.rerun()

            # Deletar usuário
            with col2:
                if st.button("🗑 Deletar", key=f"delete_{user['id']}"):

                    supabase.table("perfis") \
                        .delete() \
                        .eq("id", user["id"]) \
                        .execute()

                    st.warning("Usuário deletado.")
                    st.rerun()