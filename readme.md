# Gerador de Pseudo-palavras

Esta ferramenta, desenvolvida como parte do processo de seleção do CAEd, é um facilitador na geração de pseudo-palavras na língua portuguesa.
Pseudo palavras são importantes em auxiliar a avaliação de alfabetização de alunos.
A ferramenta pode ser acessada [aqui](http://142.93.15.216:8501/caed/).

# Banco de Palavras

A primeira parte do trabalho envolve a construção de um banco de palavras com tamanho expressivo.

 1. Primeiramente foi desenvolvido um crawler que recupera palavras do site [portaldalinguaportuguesa.org](http://www.portaldalinguaportuguesa.org/).
 2. Da letra 'a' até 'z' foram recolhidas as palavras de 500 páginas em cada letra. Cada página contém 20 palavras.
 3. Palavras idênticas entre sua escrita, divisão silábica e tonicidade foram agregadas. Um exemplo é a palavra *abacate* que aparece três vezes, como adjetivo, como substantivo masculino e feminino.
 4. Criado um arquivo **.json** com as palavras estruturadas como
 

    `{
	    "word":"zabumba",
	    "syllables":["za","bum","ba"],
	    "tonic":1, # posição 1 do vetor syllables
	    "class":"paroxítona",
	    "canonic":false
  }`

A implementação é feita em Python e utiliza as bibliotecas **requests** e **BeautifulSoup** para fazer os requests e extrair informações do resultado respectivamente. Dessa forma, obtemos do site a palavra, separação das sílabas e a sílaba tônica, e então podemos classificar por tonicidade e se ela é canônica.

## Streamlit

A ferramenta principal se alimenta do **.json** criado anteriormente. Ela é desenvolvida utilizando o framework [Streamlit](https://www.streamlit.io/).
O *Streamlit* é um framework para confecção de apps amplamente utilizado para visualização de dados. Ele é open-source e totalmente em Python (na verdade, é possível mesclar outras ferramentas/linguagens se necessário), além de dar velocidade na criação dessas visualizações por sua simplicidade.

## Gerador

O [gerador](http://142.93.15.216:8501/caed/) desenvolvido com Streamlit contém uma página informativa e outra que lhe permite customizar as palavras desejadas, adicioná-las em uma fila. Após selecionar todas as desejadas, uma lista de pseudo-palavras baseadas nas selecionadas é criada e pode ser exportada como planilha.

Um simples fluxograma do sistema pode ser visto abaixo

```mermaid
graph LR
o[Início] --> A
A[Tonicidade] --> B[Canonica]
B --> C[Buscar Palavras]
C --> D[Escolher na Lista]
D --> E[Adicionar]
E --> C
E --> o
E --> F[Limpar Tudo]
F --> o
E --> G[Gerar Pseudo-palavras]
G --> H[Exportar Planilha]
```

Com isso, o usuário pode configurar as palavras buscadas quanto sua tonicidade, se ela é ou não canônica. Com os resultados da busca ele seleciona as palavras desejadas e pode buscar novas, ou alterar a configuração inicial. 
A qualquer momento o botão Limpar pode zerar as listas e o programa volta ao estado inicial.
Ao selecionar todas as palavras desejadas é possível gerar as pseudo-palavras e exportá-las.

## Pendências e Melhorias

Ainda é necessário definir o uso da letra *y*, pois seu uso como consoante não é comum no português, e sua presença como vogal produz pseudo-palavras "fracas", facilmente detectáveis.

Tratar palavras com hífen melhor.

A heurística de geração de pseudo-palavras está muito ampla, podendo gerar as 5 palavras muito diferentes da original. Minha primeira ideia de melhoria seria utilizar algo próximo do código de Grey para gerar palavras na vizinhança da palavra selecionada, gerando assim, palavras próximas e distantes uniformemente.

## Hospedagem

O deploy da ferramenta foi feito na nuvem da [Digital Ocean](http://142.93.15.216:8501/caed/) por eu estar utilizando ela para testes e estar bem familiarizado. Um droplet básico foi criado com configuração 1 GB  Memory / 25 GB  Disk / NYC1  -  Ubuntu 18.04 (LTS) x64.



