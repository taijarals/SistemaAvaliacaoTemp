import streamlit as st
from services.supabase_client import supabase


def tela_universidades():

    st.subheader("🏫 Cadastrar Universidade")

    nome = st.text_input("Nome da Universidade")
    sigla = st.text_input("Sigla")

    logo = st.file_uploader(
        "Logo da Universidade",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Cadastrar Universidade"):

        logo_url = None

        if logo:

            file_name = f"{nome.replace(' ','_')}.png"

            supabase.storage.from_("logos-universidades").upload(
                file_name,
                logo.getvalue(),
                {"content-type": logo.type}
            )

            logo_url = supabase.storage.from_("logos-universidades").get_public_url(file_name)

        supabase.table("universidades").insert({
            "nome_universidade": nome,
            "sigla": sigla,
            "logo_url": logo_url
        }).execute()

        st.success("Universidade cadastrada!")
        st.rerun()