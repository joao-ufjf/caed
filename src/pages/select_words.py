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

tonic_options = {
    'Oxítona': 'oxitona',
    'Paroxítona': 'paroxitona',
    'Proparoxítona': 'proparoxitona'
}

canonic_options = {
    'Canônica': True,
    'Não Canônica': False
}

class Composition:

    words_df = pd.read_csv('b.csv')
    rnd_words = []
    selected_words = []
    selecting_words = False

vogals = ['a', 'e', 'i', 'o', 'u']
consoants = []
for x in range(ord('b'), ord('z') + 1):
    if chr(x) not in vogals:
        consoants.append(chr(x))

composition = Composition()

def makePseudoWord(word):
    st.write(word['word'])
    pseudo = ""
    if word['canonic']:
        for i in range(len(word['syllables'])):
            syllable = word['syllables'][i]
            st.write(syllable)
            if i == word.tonic:
                pseudo = pseudo + syllable
            else:
                pseudo = pseudo + consoants[random.randint(0, len(consoants))] + vogals[random.randint(0, len(vogals))]
                # if random.randint(0, 2):
                #     pseudo = pseudo + consoants[random.randint(0, len(consoants))] + syllable[1]
                # else:
                #     pseudo = pseudo + syllable[0] + vogals[random.randint(0, len(vogals))]
    else:
        st.write("syllable")
        pseudo = word['word']

    return pseudo


def write():
    st.title("Escolha das Palavras:")

    st.subheader("Escolha uma configuração")

    tonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(tonic_options.keys()))
    canonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(canonic_options.keys()))
    
    composition.selecting_words = True

    st.subheader("Busque palavras")
    if st.button("Clique para buscar palavras"):
        composition.rnd_words = random.sample(range(0, len(composition.words_df)), min(5, len(composition.words_df)))

    # st.dataframe(composition.words_df.loc[composition.rnd_words])

    selected = st.multiselect(
        'Selecione as palavras desejadas',
        list(composition.words_df.loc[composition.rnd_words]['word']))

    # st.write(selected)

    if st.button("Adicionar Palavras"):
        composition.selected_words = composition.selected_words + selected

    st.title("Geração de Pseudo-palavras:")

    st.subheader("Palavras selecionadas:")
    sliced_df = composition.words_df.loc[composition.words_df['word'].isin(composition.selected_words)]
    st.dataframe(sliced_df)

    for i, word in sliced_df.iterrows():
        st.write(makePseudoWord(word))

    # with st.spinner(f"Loading {menu_selection} ..."):
        # display.render_page(menu)

    # st.sidebar.info(
    #     "https://github.com/Avkash/demoapps"
    # )
    # st.sidebar.info(
    #     "demoapps/StreamlitApp"
    # )

if __name__ == "__main__":
    # composition = Composition()
    main()