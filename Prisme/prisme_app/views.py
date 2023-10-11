from django.shortcuts import render
from .utils import linhas
# Create your views here.
'''exemplo de gráfico
def view(request):
    query = Modelo.objects.all
    x = [x.atributo for x in query]
    y = [y.atributo for y in query]
    grafico = linhas(x, y, titulo="título", tit_x="titulo col x", tit_y = "titulo col y)
    return(request, "arquivo.html", {"graf_linha": grafico}
    
exemplo html
<img src=data:image/png;base64, {{ graf_linha safe }}
'''