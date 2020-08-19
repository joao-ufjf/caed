# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import random

import display
import src.pages.select_words
import src.pages.select_pseudo_words

MENU = {
    "Seleção de Palavras" : src.pages.select_words,
    "Geração de pseudo Palavras" : src.pages.select_pseudo_words
}

def main():
    st.sidebar.title("O que deseja fazer?")
    menu_selection = st.sidebar.radio("Escolha uma opção", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        display.render_page(menu)

if __name__ == "__main__":
    # composition = Composition()
    main()