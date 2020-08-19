import streamlit as st
import pandas as pd
import numpy as np
from numpy import random
import os
import io
import glob
import base64

# Função para fazer download de pd.DataFrame como uma Sheet de um xlsx

class group:
    score = 0 # média dos scores individuais
    count = 0
    percernt = 0 # count/total

    def func(self):
        return 0

def write():
    
    #
    #  Início
    #

    ##### Título
    st.title('Pseudo Palavras')

    