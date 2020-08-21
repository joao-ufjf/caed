# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import random
import copy

import display
import src.pages.select_pseudo_words

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

    words_df = pd.read_json('data/b.json', orient = "index")
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
    # st.write(word['word'])
    pseudo = copy.deepcopy(word)
    pseudo['word'] = ''
    pseudo['syllables'] = []
    if word['canonic']:
        # st.write("  canonic" + str(len(word['syllables'])))
        for i in range(len(word['syllables'])):
            syllable = word['syllables'][i]
            # st.write("    " + syllable)
            if i == int(word.tonic):
                pseudo['syllables'].append(syllable)
                pseudo['word'] = pseudo['word'] + syllable
            else:
                # pseudo = pseudo + consoants[random.randint(0, len(consoants))] + vogals[random.randint(0, len(vogals))]
                if random.randint(0, 2):
                    consoant = consoants[random.randint(0, 20)]
                    new_syllable = consoant + syllable[1]
                    pseudo['syllables'].append(new_syllable)
                    pseudo['word'] = pseudo['word'] + new_syllable
                else:
                    vogal = vogals[random.randint(0, 4)]
                    new_syllable = syllable[0] + vogal
                    pseudo['syllables'].append(new_syllable)
                    pseudo['word'] = pseudo['word'] + new_syllable
    else:
        # st.write("  not canonic")
        pseudo['word'] = "bananice"
        pseudo['syllables'] = []

    return pseudo


def write():
    st.title("Gerador de Pseudo-palavras")

    st.write("""
        Uma forma de avaliar a capacidade de leitura de uma criança é verificar a capacidade de decodificação. Para isso, costuma-se utilizar testes 
        com palavras e com pseudo-palavras, ou seja, palavras que não existem na língua portuguesa, mas que são palavras “corretas”.
        Exemplos de pseudo-palavras são comalo, rupeita, lopi. Não são exemplos de pseudo-palavras o que não faz
        sentido na sintaxe da língua portuguesa como sunpa, crippa, treazsa. Essa aplicação foi desenvolvida com o objetivo de 
        prover uma ferramenta ao avaliador para gerar os testes de pseudo-palavras.
    """)

    st.header("Escolha das Palavras:")

    st.write("Aqui o avaliador deve escolher as características da palavra, em seguida selecionar as desejadas para gerar pseudo-palavras.")

    st.subheader("Escolha uma configuração")

    tonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(tonic_options.keys()))
    canonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(canonic_options.keys()))
    
    composition.selecting_words = True

    # st.write(composition.words_df)

    st.subheader("Busque palavras nessa configuração")
    st.write("""
        Ao buscar palavras, serão apresentadas 30 palavras do banco de palavras, 
        onde podem ser selecionadas diversas delas. Ao buscar novamente outras 30 
        palavras são recuperas do banco de palavras.
    """)
    if st.button("Buscar palavras"):
        composition.rnd_words = random.sample(range(0, len(composition.words_df)), min(15, len(composition.words_df)))

    # st.dataframe(composition.words_df.loc[composition.rnd_words])

    selected = st.multiselect(
        'Selecione as palavras desejadas',
        list(composition.words_df.loc[composition.rnd_words]['word']))

    st.write("""
        Ao adicionar palavras, elas vão para a lista de palavras utilizadas para gerar pseudo-palavras.
    """)

    if st.button("Adicionar palavras"):
        composition.selected_words = composition.selected_words + selected

    st.header("Geração de Pseudo-palavras:")

    st.subheader("Palavras selecionadas:")
    sliced_df = composition.words_df.loc[composition.words_df['word'].isin(composition.selected_words)]
    st.dataframe(sliced_df)

    st.write("""
        Ao clicar no botão "Gerar", serão geradas de 2 a 5 pseudo-palavras para cada palavra selecionada.
        Clicar no botão novamente gera outras pseudo-palavras.
    """)

    st.subheader("Gerar pseudo-palavras:")
    if st.button("Gerar"):
        pseudo_words = pd.DataFrame(columns = sliced_df.columns)
        n_pw = 0
        for i, word in sliced_df.iterrows():
            for j in range(random.randint(2, 5)):
                pseudo_words.loc[n_pw] = makePseudoWord(word)
                n_pw = n_pw + 1

        st.dataframe(pseudo_words)

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