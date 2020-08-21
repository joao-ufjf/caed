# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import random

import display
import src.pages.select_words
import src.pages.info

MENU = {
    "Informações" : src.pages.info,
    "Gerador" : src.pages.select_words
}

def main():
    st.markdown(f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: 60%;
            }}
            .reportview-container .main {{
            }}
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Páginas:")
    menu_selection = st.sidebar.radio("Escolha uma opção", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        display.render_page(menu)

    st.sidebar.header("Infos:")
    st.sidebar.info(
        "https://github.com/Joao-ufjf/caed"
    )

if __name__ == "__main__":
    # composition = Composition()
    main()