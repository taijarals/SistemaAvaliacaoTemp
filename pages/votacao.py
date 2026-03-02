import streamlit as st
from services.supabase_client import supabase

def buscar_disciplinas():
    response = supabase.table("disciplinas").select("*").execute()
    return response.data if response.data else []

def tela_votacao():

    st.title("Sistema de Votação")

    nome = st.text_input("Nome Completo")

    disciplinas = buscar_disciplinas()

    if not disciplinas:
        st.warning("Nenhuma disciplina cadastrada.")
        return

    opcoes = [
        f"{d['nome_disciplina']} - {d['nome_curso']} ({d['dia_aula']})"
        for d in disciplinas
    ]

    escolha = st.selectbox("Disciplina", opcoes)

    apresentacao = st.slider("1 - Apresentação", 1, 5)
    conhecimento = st.slider("2 - Conhecimento", 1, 5)
    aderencia = st.slider("3 - Aderência ao Tema", 1, 5)
    resolutividade = st.slider("4 - Resolutividade", 1, 5)
    criatividade = st.slider("5 - Criatividade", 1, 5)

    soma = apresentacao + conhecimento + aderencia + resolutividade + criatividade
    nota_final = soma / 25

    st.info(f"Nota Final (máx 1.0): {round(nota_final, 3)}")

    if st.button("Enviar votação"):
        if nome.strip() == "":
            st.warning("Informe seu nome.")
            return

        disciplina_selecionada = disciplinas[opcoes.index(escolha)]

        supabase.table("votos").insert({
            "nome": nome,
            "curso": disciplina_selecionada["nome_curso"],
            "disciplina": disciplina_selecionada["nome_disciplina"],
            "apresentacao": apresentacao,
            "conhecimento": conhecimento,
            "aderencia": aderencia,
            "resolutividade": resolutividade,
            "criatividade": criatividade,
            "media": nota_final
        }).execute()

        st.success("Voto registrado!")