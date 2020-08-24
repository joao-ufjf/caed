# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import random
import copy
import io
import base64
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.writer.excel import save_virtual_workbook

import display

tonic_options = {
    'Oxítona': 'oxítona',
    'Paroxítona': 'paroxítona',
    'Proparoxítona': 'proparoxítona'
}

canonic_options = {
    'Canônica': True,
    'Não Canônica': False
}

class Composition:

    words_df = pd.read_json('data/b.json', orient = "index")
    rnd_words = []
    selected_words = []
    selecting_words = None

vogals = ['a', 'e', 'i', 'o', 'u']
consoants = []
for x in range(ord('b'), ord('z') + 1):
    if chr(x) not in vogals:
        consoants.append(chr(x))

composition = Composition()

def makePseudoWord(word):
    """
    A função deve retornar uma pseudo-palavra parecida e com as mesmas propriedades
    """

    # st.write(word['word'])
    pseudo = copy.deepcopy(word)
    pseudo['word'] = ''
    pseudo['syllables'] = []
    if word['canonic']: # No caso de uma palavra canônica preservamos a sílaba tônica
        for i in range(len(word['syllables'])):
            syllable = word['syllables'][i]
            if i == int(word.tonic): # Mantém a sílaba tônica
                pseudo['syllables'].append(syllable)
                pseudo['word'] = pseudo['word'] + syllable
            else: # Se não é tõnica, decido o que fazer
                if random.randint(0, 2): # 50% de chande de manter a consoante
                    consoant = consoants[random.randint(0, 20)]
                    new_syllable = consoant + syllable[1]
                    pseudo['syllables'].append(new_syllable)
                    pseudo['word'] = pseudo['word'] + new_syllable
                else: # 50% de chande de manter a vogal
                    vogal = vogals[random.randint(0, 4)]
                    new_syllable = syllable[0] + vogal
                    pseudo['syllables'].append(new_syllable)
                    pseudo['word'] = pseudo['word'] + new_syllable
    else: # No caso de não ser canônica mantemos a sílaba tônica
        for i in range(len(word['syllables'])):
            syllable = word['syllables'][i]
            # st.write("    " + syllable)
            if i == int(word.tonic): # Mantém a sílaba tônica
                pseudo['syllables'].append(syllable)
                pseudo['word'] = pseudo['word'] + syllable
            else: # Se não é tõnica, decido o que fazer
                new_syllable = ''
                for c in syllable:
                    if c in vogals: # Troca a vogal por outra
                        new_syllable = new_syllable + vogals[random.randint(0, 4)]
                    else: # Troca a consoante por outra
                        new_syllable = new_syllable + consoants[random.randint(0, 20)]
                pseudo['syllables'].append(new_syllable)
                pseudo['word'] = pseudo['word'] + new_syllable

    return pseudo

def to_excell(df, name):
    wb = Workbook()
    ws = wb.active

    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    vw = save_virtual_workbook(wb)
    xlsx_io = io.BytesIO(vw)
    xlsx_io.seek(0)
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    
    st.markdown(f'<a href="{href_data_downloadable}" download="template.xlsx">{name}</a>', unsafe_allow_html=True)

def write():
    if st.sidebar.button("Limpar Projeto"):
        composition.selected_words = []

    st.title("Gerador de Pseudo-palavras")

    st.write("""
        Essa aplicação foi desenvolvida com o objetivo de 
        prover uma ferramenta ao avaliador para gerar os 
        testes de pseudo-palavras. 
        Mais informações e conceitos na aba **informações**.
    """)

    st.header("Escolha das Palavras:")

    st.write("Aqui o avaliador deve escolher as características da palavra, em seguida selecionar as desejadas para gerar pseudo-palavras.")

    st.subheader("Escolha uma configuração")

    tonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(tonic_options.keys()))
    canonic_selection = st.radio("Escolha uma opção quanto à sílaba tônica", list(canonic_options.keys()))
    

    # st.write(composition.words_df)

    st.subheader("Busque palavras nessa configuração")
    st.write("""
        Serão apresentadas até 30 palavras do banco de palavras, 
        onde podem ser selecionadas diversas delas. Ao buscar novamente outras 
        palavras são recuperas do banco de palavras.
    """)
    if st.button("Buscar palavras"):
        # Filtra os dados com a configuração selecionada
        composition.selecting_words = composition.words_df[composition.words_df['class'] == tonic_options[tonic_selection]]
        composition.selecting_words = composition.selecting_words[composition.selecting_words['canonic'] == canonic_options[canonic_selection]]
        # Seleciona até 30 palavras aleatórias
        composition.rnd_words = random.sample(list(composition.selecting_words.index), min(30, len(composition.selecting_words)))
        composition.selecting_words = composition.selecting_words.loc[composition.rnd_words]

    # st.dataframe(composition.selecting_words)

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

    # Valores repetidos não entram
    # TODO ao atualizar a página não está resetando no heroku, apenas em sessões locais
    composition.selected_words = list(set(composition.selected_words))
    to_use = st.multiselect(
        '',
        composition.selected_words, 
        composition.selected_words)

    # Recupera os registros que contém as palavras selecionadas
    sliced_df = composition.words_df.loc[composition.words_df['word'].isin(to_use)]
    st.dataframe(sliced_df)

    st.write("""
        Ao clicar no botão "Gerar", serão geradas de 2 a 5 pseudo-palavras para cada palavra selecionada.
        Clicar no botão novamente gera outras pseudo-palavras.
    """)

    st.subheader("Gerar pseudo-palavras:")
    if st.button("Gerar"):
        # É criado um DataFrame com as colunas originais
        pseudo_words = pd.DataFrame(columns = sliced_df.columns)
        n_pw = 0
        for i, word in sliced_df.iterrows():
            for j in range(random.randint(2, 5)): # Para cada palavra são geradas de 2 a 5 pseudo-palavras
                pseudo_words.loc[n_pw] = makePseudoWord(word)
                n_pw = n_pw + 1

        st.dataframe(pseudo_words)

        def listToString(s):          
            # initialize an empty string 
            str1 = "-" 
            
            # return string   
            return (str1.join(s))

        pseudo_words["syllables"] = pseudo_words["syllables"].apply(listToString)
        to_excell(pseudo_words, "Download das Pseudo-palavras")


if __name__ == "__main__":
    # composition = Composition()
    main()