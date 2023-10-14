import pandas as pd
from django.shortcuts import render, redirect
from .utils import linhas, barras
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Projeto, Ong, DadosImpactos, LinhasImpacto

# Create your views here.

tipos1 = [
         "Selecione o tipo de dado Numérico",
         "Pessoas Impactadas",
         "Casas Contruidas",
         "Valor"
     ]

tipos2 = [
    "Selecione o tipo de dado Categorico",
    "Tempo",
    "Pessoas",
]


#@login_required
def home(request):
    graficos = []
    indice = 0
    contexto = {
    }
    usuario = request.user
    try:
        ong = Ong.objects.get(nome=usuario.first_name)
    except:
        redirect(login)
    else:
        projetos = ong.projeto_set.all()
        for projeto in list(projetos):
            dados = projeto.dadosimpactos_set.all()
            for dado in list(dados):
                linha = dado.linhasimpacto_set.all().values()
                if linha is not None:
                    base = pd.DataFrame(linha)
                    grafico = linhas(base["valor2"], base["valor1"], dado.titulo, dado.tipo2, dado.tipo1)
                    indice += 1
                    graficos.append(grafico)
        contexto["grafico"] = graficos
        return render(request, "home.html", context=contexto)

#@login_required
def add_di(request):
    contexto = {

    }
    return render(request, "dados.html", context=contexto)

#@login_required
def teste(request):
    usuario = request.user

    contexto={
        "grafico": linhas([1,2,3], [20,30,40], "p", "pX", "pY")
    }
    return render(request, "ex.html", context=contexto)


def Login(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return render(request, "login.html", {"erro": "Usuário não encontrado"})
    return render(request, "login.html")


def Logout(request):
    logout(request)
    
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect(home)


@login_required
def add_projeto(request):
    erros = {}
    usuario = request.user
    ong_logada = Ong.objects.get(nome=usuario.first_name) 
    
    nome_projeto = ""
    descricao = ""
    metodologiasUtilizadas = ""
    publicoAlvo = ""
    
    if request.method == 'POST':
        errado = False
        nome_projeto = request.POST['nome_projeto']
        descricao = request.POST['descricao']
        metodologiasUtilizadas = request.POST['metodologia']
        publicoAlvo = request.POST['publico']
        dataDeCriacao = request.POST['criacao']

        if not nome_projeto or not descricao or not metodologiasUtilizadas or not publicoAlvo or not dataDeCriacao:
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True

        if errado:
            contexto = {
                "erros": erros,
                "ong": usuario.first_name,
                "nome_projeto": nome_projeto,
                "descricao": descricao,
                "metodologiasUtilizadas": metodologiasUtilizadas,
                "publicoAlvo": publicoAlvo,
            }
            return render(request, "add_projeto.html", contexto)
            
        if Projeto.objects.filter(nome_projeto=nome_projeto).exists():
            return render(request, 'add_projeto.html', {"erro": "Esse Projeto já existe"})
        
        try:
            Projeto.objects.create(ong=ong_logada, nome_projeto=nome_projeto, descricao=descricao, metodologiasUtilizadas=metodologiasUtilizadas, publicoAlvo=publicoAlvo,
                                   dataDeCriacao=dataDeCriacao)
        finally:
            return render(request, 'add_dados.html')

    contexto = {
        "erros": erros,
        "ong": usuario.first_name,
        "nome_projeto": nome_projeto,
        "descricao": descricao,
        "metodologiasUtilizadas": metodologiasUtilizadas,
        "publicoAlvo": publicoAlvo,
    }
    return render(request, 'add_projeto.html', contexto)

@login_required
def add_dados(request):
    usuario = request.user
    erros = {}
    if request.method == 'POST':
        errado = False
        projeto = request.POST['projeto']
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        valor1 = request.POST['valor1']
        valor2 = request.POST['valor2']
        tipo1 = request.POST['tipo1']
        tipo2 = request.POST['tipo2']

        if not projeto or not descricao or not titulo or not valor1 or not valor2 or tipo1 == "Selecione o tipo de dado" or tipo2 == "Selecione o tipo de dado":
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True
        
        if errado:
                contexto = {
                    "erros": erros,
                    "projeto": projeto,
                    "descricao": descricao,
                    "titulo": titulo,
                    "valor1": valor1,
                    "valor2":valor1,
                    "tipo1":tipo1,
                    "tipo2": tipo2,
                    "tipos1":tipos1,
                    "tipos2": tipos2
                }
                return render(request, "add_dados.html", contexto)
        
        if DadosImpactos.objects.filter(titulo=titulo).exists():
            return render(request, 'add_projeto.html', {"erro": "Esse Dado já existe"})
        if Projeto.objects.filter(nome_projeto=projeto).exists():
            DadosImpactos.objects.create(projeto=Projeto.objects.filter(nome_projeto=projeto).first(),titulo=titulo,descricao=descricao,tipo1=tipo1,tipo2=tipo2)
            return redirect(home)
        else:
            return render(request, 'add_dados.html', {"erro": "Essa Projeto Não existe"})

    return render(request,'add_dados.html',{"tipos1":tipos1, "tipos2":tipos2})


@login_required
def add_valores(request):
    usuario = request.user
