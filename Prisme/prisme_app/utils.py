import matplotlib.pyplot as plt
import base64
from io import BytesIO


def salvagrafico():
    buffer = BytesIO
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagem_png = buffer.getvalue()
    grafico = base64.b64encode(imagem_png)
    grafico = grafico.decode("utf-8")
    buffer.close()
    return grafico


def linhas(x, y, titulo, tit_x, tit_y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(titulo)
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    plt.tight_layout
    grafico = salvagrafico()
    return grafico
