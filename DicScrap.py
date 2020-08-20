# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unidecode

# Lista caracteres de c1 a c2
def char_range(c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

# Classifica a palavra pela sílaba tônica
def wclass(length, tonic):
    dif = length - tonic
    if dif == 1:
        return 'oxítona'
    elif dif == 2:
        return 'paroxítona'
    elif dif > 2:
        return 'proparoxítona'

vogals = ['a', 'e', 'i', 'o', 'u']
consoants = [chr(x) if chr(x) not in vogals else None for x in range(ord('b'), ord('z') + 1)]

def isVogal(x):
    return unidecode.unidecode(x) in vogals

def isConsoant(x):
    return unidecode.unidecode(x) in consoants

first = 'a'
last = 'b'
pages = 10

# Recupera as palavras de a até z
for c in char_range(first, last):
    n_words = 0
    print("Gathering " + c, end = '')

    df = pd.DataFrame(columns=['word', 'syllables', 'tonic', 'class', 'canonic'])
    # Recuperando 100 páginas com 20 resultados, no máximo 2000 palavras por letra
    for p in range(0, pages):
        page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=fonetica&region=rjx&act=list&letter={0}&start={1}'.format(c, p * 20))
        soup = BeautifulSoup(page.text, 'html.parser')
        for a in soup.find_all(title = 'Palavra'):
            word = {
                "word": '',
                "syllables": [],
                "tonic": 0,
                "class": None
            }
            t_count = 0
            for x in a.find('a'):
                if x.name != None:
                    #contains the tonic syllable
                    if x.name == 'u' :
                        word['word'] = word['word'] + re.sub('\n', '', x.string)
                        word['syllables'].append(re.sub('\n', '', x.string))
                        word['tonic'] = t_count
                        t_count = t_count + 1
                else:
                    word['word'] = word['word'] + re.sub('\n', '', x)
                    # hyphen does not count as a syllable
                    if x != '-':
                        word['syllables'].append(re.sub('\n', '', x))
                        t_count = t_count + 1
            word['class'] = wclass(len(word['syllables']), word['tonic'])

            word['canonic'] = True
            for syllable in word['syllables']:
                if len(syllable) != 2:
                    word['canonic'] = False
                    break
                elif not (isConsoant(syllable[0]) & isVogal(syllable[1])):
                    word['canonic'] = False
                    break
            
            df.loc[n_words] = [ word['word'], word['syllables'], word['tonic'], word['class'], word['canonic']]
            n_words = n_words + 1
    
    df = df.drop_duplicates(subset = ['word', 'tonic', 'class'])

    # improve
    df.index = [i for i in range(0, len(df))]
    df.to_json(c + '.json', orient = "index")
    print(" with " + str(len(df)) + " words")
            