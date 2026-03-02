import streamlit as st
from pages.votacao import tela_votacao
from pages.admin import tela_admin

st.set_page_config(page_title="Sistema de Avaliação")

menu = st.sidebar.selectbox(
    "Menu",
    ["Votação", "Admin"]
)

if menu == "Votação":
    tela_votacao()
else:
    tela_admin()