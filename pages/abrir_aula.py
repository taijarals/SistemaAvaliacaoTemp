import streamlit as st
import uuid
import qrcode
from services.supabase_client import supabase


def buscar_disciplinas():
    response = supabase.table("disciplinas").select("*").execute()
    return response.data if response.data else []


def tela_abrir_aula():

    st.title("Abrir Aula")

    disciplinas = buscar_disciplinas()

    if not disciplinas:
        st.warning("Nenhuma disciplina cadastrada.")
        return

    opcoes = [
        f"{d.get('nome_disciplina')} ({d.get('dia_aula')})"
        for d in disciplinas
    ]

    escolha = st.selectbox("Disciplina", opcoes)

    if st.button("Abrir aula"):

        disciplina_selecionada = disciplinas[opcoes.index(escolha)]

        codigo = str(uuid.uuid4())

        aula = supabase.table("aulas").insert({
            "disciplina": disciplina_selecionada["nome_disciplina"],
            "codigo_checkin": codigo
        }).execute()

        link = f"https://seuapp.streamlit.app/checkin?codigo={codigo}"

        qr = qrcode.make(link)
        qr.save("qrcode.png")

        st.success("Aula aberta!")

        st.image("qrcode.png")
        st.write("Peça aos alunos para escanear o QRCode")