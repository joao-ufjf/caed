import streamlit as st

# Função para fazer download de pd.DataFrame como uma Sheet de um xlsx

def write():

    ##### Título
    st.title("Informações")

    st.header("Começando")

    st.subheader("Menu Lateral")
    st.write("""
        O menu lateral traz a navegação entre esta página e o 
        **Gerador de Pseudo-palavras**, além de informações básicas.
    """)

    st.subheader("Reiniciando o Projeto")
    st.write("""
        Para recomeçar seu trabalho, limpar todos os campos, basta apenas recarregar a página.
    """)

    st.subheader("Mãos na Massa")
    st.write("""
        Após passar pelos conceitos, fique livre para acessar o **Gerador de Pseudo-palavras** no menu lateral.
    """)

    st.header("Conceitos")

    st.subheader("Pseudo-palavras")
    st.write("""
        Pseudo-palavras são palavras que não existem na língua portuguesa, mas que são palavras “corretas”.
        Exemplos de pseudo-palavras são comalo, rupeita, lopi. Não são exemplos de pseudo-palavras o que não faz
        sentido na sintaxe da língua portuguesa como sunpa, crippa, treazsa.
    """)

    st.subheader("Palavra Canônica")
    st.write("""
        Uma palavra canônica é
        aquela que contém sílabas sempre do tipo CV (consoante + vogal), como cabeça, canela, janela, luta, sopa,
        etc. Exemplos de palavras não canônicas são: abajur, lápis, cansado, asa, alheio, etc. Ou seja, palavras
        que tem alguma sílaba que não seja no formato CV.
    """)

    st.subheader("Tonicidade")
    st.write("""
        A tonicidade é a classificação de palavras quanto a posição de sua sílaba tônica.
    """)
    st.markdown('A **oxítona** possui a sílaba tônica na última posição da palavra.')
    st.markdown('A **paroxítona** tem sua sílaba tônica na penúltima posição.')
    st.markdown('**Proparoxítonas** existem quando a sílaba tônica ocorre na antepenúltima posição da palavra.')

    st.header("Sobre o Gerador")

    st.subheader("Como ele faz as pseudo-palavras?")
    st.write("""
        Existem alguns casos considerados para gerar uma pseudo-palavra
        baseada em uma palavra real.
    """)
    st.write("""
        Se a palavra é canôninca, navegamos sílaba a sílaba dela. 
        Se a sílaba é a tônica, ela é repetida na pseudo-palavra.
        Se não é a sílaba tônica, existe 50% de chance de manter 
        a consoante ou a vogal, sorteando a outra letra.
    """)
    st.write("""
        Se a palavra não é canôninca, navegamos sílaba a sílaba dela.
        A sílaba tônica também é repetida.
        Se não é a sílaba tônica, cada letra é sorteada novamente, mantendo consoantes e vogais nas posições originais.             
    """
    )
    st.write("""
        Dessa forma, temos pseudo-palavras próximas das originais.
    """)

    st.subheader("Próximos Passos")
    st.write("""
        Definir o uso da letra y, funcionando como vogal ou consoante.
    """)