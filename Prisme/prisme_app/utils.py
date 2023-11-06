import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import pandas as pd
import random
import array


def salvagrafico():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagem_png = buffer.getvalue()
    grafico = base64.b64encode(imagem_png)
    grafico = grafico.decode("utf-8")
    buffer.close()
    return grafico


def linhas(x, y, titulo, tit_x, tit_y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7.5,5))
    plt.title(titulo)
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    plt.tight_layout()
    grafico = salvagrafico()
    return grafico

def barras(base, categorica, numerica, titulo, tit_x, tit_y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(10,5))
    agrupado = base.groupby([categorica])[numerica].sum()
    #tit_x é categorico
    sns.barplot(x=tit_x, y=tit_y, data=agrupado).set_title(titulo)
    plt.tight_layout()
    grafico = salvagrafico()
    return grafico


def criador_senha_aleatoria(tamanho):
    MAX_LEN = tamanho
    DIGITOS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LETRAS_MINUSCULAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r',
                         's','t', 'u', 'v', 'w', 'x', 'y','z']
    LETRAS_MAIUSCULAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q','R',
                        'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']

    LISTA_COMBINADA = DIGITOS + LETRAS_MINUSCULAS + LETRAS_MAIUSCULAS

    rand_digit = random.choice(DIGITOS)
    rand_upper = random.choice(LETRAS_MINUSCULAS)
    rand_lower = random.choice(LETRAS_MAIUSCULAS)
    temp_code= rand_digit + rand_upper + rand_lower

    for x in range(MAX_LEN - 4):
        temp_code= temp_code+ random.choice(LISTA_COMBINADA)
        temp_pass_list = array.array('u', temp_code)
        random.shuffle(temp_pass_list)

    codigo = ""

    for x in temp_pass_list:
        codigo = codigo + x

    return codigo