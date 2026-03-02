import streamlit as st
from supabase import create_client
import pandas as pd

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Sistema de Votação", layout="centered")

# =========================
# MENU LATERAL
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Votação", "Painel Administrativo"]
)

# =========================
# TELA DE VOTAÇÃO
# =========================
if menu == "Votação":

    st.title("Sistema de Votação")

    nome = st.text_input("Nome Completo")

    curso = st.selectbox("Curso", [
        "Engenharia da Computação",
        "Ciência da Computação",
        "Sistemas de Informação"
    ])

    disciplina = st.selectbox("Disciplina", [
        "Estrutura de Dados",
        "Banco de Dados",
        "Algoritmos"
    ])

    st.divider()
    st.subheader("Avaliação (1 a 5)")

    apresentacao = st.slider("1 - Apresentação", 1, 5)
    conhecimento = st.slider("2 - Conhecimento", 1, 5)
    aderencia = st.slider("3 - Aderência ao Tema", 1, 5)
    resolutividade = st.slider("4 - Resolutividade", 1, 5)
    criatividade = st.slider("5 - Criatividade", 1, 5)

    # -------------------------
    # CÁLCULO DA NOTA NORMALIZADA
    # -------------------------
    soma = (
        apresentacao +
        conhecimento +
        aderencia +
        resolutividade +
        criatividade
    )

    nota_final = soma / 25  # máximo = 1.0

    st.info(f"Nota Final (máx 1.0): {round(nota_final, 3)}")

    if st.button("Enviar votação"):

        if nome.strip() == "":
            st.warning("Por favor, informe seu nome completo.")
        else:

            dados = {
                "nome": nome.strip(),
                "curso": curso,
                "disciplina": disciplina,
                "apresentacao": apresentacao,
                "conhecimento": conhecimento,
                "aderencia": aderencia,
                "resolutividade": resolutividade,
                "criatividade": criatividade,
                "media": nota_final
            }

            try:
                supabase.table("votos").insert(dados).execute()
                st.success(f"Voto registrado com sucesso! Nota final: {round(nota_final, 3)}")
            except Exception:
                st.error("Você já votou nessa disciplina!")

# =========================
# PAINEL ADMINISTRATIVO
# =========================
elif menu == "Painel Administrativo":

    st.title("Painel Administrativo")

    response = supabase.table("votos").select("*").execute()

    if response.data:

        df = pd.DataFrame(response.data)

        st.subheader("Todos os votos")
        st.dataframe(df)

        st.divider()

        # -------------------------
        # MÉDIA POR DISCIPLINA
        # -------------------------
        st.subheader("Média por Disciplina")

        medias = (
            df.groupby("disciplina")["media"]
            .mean()
            .reset_index()
        )

        medias["media"] = medias["media"].round(3)

        medias = medias.sort_values(by="media", ascending=False)

        st.dataframe(medias)

        st.divider()

        # -------------------------
        # RANKING
        # -------------------------
        st.subheader("🏆 Ranking")

        ranking = medias.copy()
        ranking["posição"] = range(1, len(ranking) + 1)

        st.dataframe(ranking)

    else:
        st.info("Nenhum voto registrado ainda.")