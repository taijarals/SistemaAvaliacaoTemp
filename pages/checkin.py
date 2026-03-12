import streamlit as st
from services.supabase_client import supabase


def buscar_aula_por_codigo(codigo):

    response = supabase.table("aulas") \
        .select("*") \
        .eq("codigo_checkin", codigo) \
        .execute()

    return response.data[0] if response.data else None


def tela_checkin():

    st.title("Check-in da Aula")

    codigo = st.query_params.get("codigo")

    if not codigo:
        st.error("QR Code inválido.")
        return

    aula = buscar_aula_por_codigo(codigo)

    if not aula:
        st.error("Aula não encontrada.")
        return

    aluno = st.text_input("Nome ou matrícula")

    if st.button("Confirmar presença"):

        if aluno.strip() == "":
            st.warning("Informe seu nome ou matrícula.")
            return

        supabase.table("presencas").insert({
            "aula_id": aula["id"],
            "aluno_id": aluno
        }).execute()

        st.success("Presença registrada!")