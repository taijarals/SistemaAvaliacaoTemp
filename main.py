import streamlit as st

st.set_page_config(page_title="Sistema de Votação", layout="centered")

# -------------------------
# Inicialização do estado
# -------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = 1

if "dados_usuario" not in st.session_state:
    st.session_state.dados_usuario = {}

# -------------------------
# LISTAS FIXAS
# -------------------------
cursos = [
    "Engenharia da Computação",
    "Ciência da Computação",
    "Sistemas de Informação",
    "Análise e Desenvolvimento de Sistemas"
]

disciplinas = [
    "Estrutura de Dados",
    "Banco de Dados",
    "Algoritmos",
    "Programação Web"
]

# =========================
# TELA 1 - IDENTIFICAÇÃO
# =========================
if st.session_state.pagina == 1:
    
    st.title("Sistema de Votação")
    st.subheader("Identificação do Aluno")

    nome = st.text_input("Nome Completo")
    curso = st.selectbox("Curso", cursos)
    disciplina = st.selectbox("Disciplina", disciplinas)

    if st.button("Ir para votação"):
        if nome.strip() == "":
            st.warning("Por favor, preencha seu nome completo.")
        else:
            st.session_state.dados_usuario = {
                "nome": nome,
                "curso": curso,
                "disciplina": disciplina
            }
            st.session_state.pagina = 2
            st.rerun()

# =========================
# TELA 2 - VOTAÇÃO
# =========================
elif st.session_state.pagina == 2:
    
    st.title("Avaliação")

    st.write("### Avaliador:")
    st.write(f"**Nome:** {st.session_state.dados_usuario['nome']}")
    st.write(f"**Curso:** {st.session_state.dados_usuario['curso']}")
    st.write(f"**Disciplina:** {st.session_state.dados_usuario['disciplina']}")
    
    st.divider()

    st.write("### Dê uma nota de 1 a 5:")

    apresentacao = st.slider("1 - Apresentação", 1, 5)
    conhecimento = st.slider("2 - Conhecimento", 1, 5)
    aderencia = st.slider("3 - Aderência ao Tema", 1, 5)
    resolutividade = st.slider("4 - Resolutividade", 1, 5)
    criatividade = st.slider("5 - Criatividade", 1, 5)

    if st.button("Enviar votação"):
        
        resultado = {
            "Apresentação": apresentacao,
            "Conhecimento": conhecimento,
            "Aderência ao Tema": aderencia,
            "Resolutividade": resolutividade,
            "Criatividade": criatividade
        }

        st.success("Votação registrada com sucesso!")

        st.write("### Notas enviadas:")
        st.json(resultado)

        # Aqui você pode salvar em banco depois