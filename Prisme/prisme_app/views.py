import pandas as pd
import statistics as sts
from django.shortcuts import render, redirect
from .utils import linhas, barras
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Projeto, Ong, DadosImpactos, LinhasImpacto


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


def Login(request):
    if request.user != None:
        redirect(home)
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


def home(request):
    moda = True
    usuario = request.user
    graficos = []
    impactados = []
    contexto = {}

    try:
        ong = Ong.objects.get(nome=usuario.first_name)
    except:
        return redirect(Login)
    else:
        projetos = ong.projeto_set.all()
        for projeto in list(projetos):
            dados = projeto.dadosimpactos_set.all()
            for dado in list(dados):
                impactados.append(dado.tipo1)
                linha = dado.linhasimpacto_set.all().values()
                if len(list(linha)) != 0:
                    base = pd.DataFrame(linha)
                    grafico = linhas(base["valor2"], base["valor1"], dado.titulo, dado.tipo2, dado.tipo1)
                    graficos.append(grafico)
        contexto["grafico"] = graficos
        try:
            moda_impacto = sts.mode(impactados) #nome da moda
        except:
            moda_impacto = "Sem dados suficientes"
            moda = False
        else:
            for indice, projeto in enumerate(list(projetos)):
                dados = projeto.dadosimpactos_set.all()
                for dado in list(dados):
                    if dado.tipo1 == moda_impacto:
                        linha = dado.linhasimpacto_set.all().values()
                        if len(list(linha)) != 0:
                            if indice == 0:
                                base_impacto = pd.DataFrame(linha)
                            else:
                                moda = True
                                base_impacto_temp = pd.DataFrame(linha)
                                base_impacto = pd.concat([base_impacto, base_impacto_temp])
                        else:
                            moda = False
        contexto["nome_impacto"] = moda_impacto
        if moda:
            contexto["soma_impacto"] = base_impacto['valor1'].sum()
        else:
            contexto["soma_impacto"] = 0


        return render(request, "home.html", context=contexto)


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
            contexto = {
                "erros": "Esse Projeto já existe",
                "ong": usuario.first_name,
                "nome_projeto": nome_projeto,
                "descricao": descricao,
                "metodologiasUtilizadas": metodologiasUtilizadas,
                "publicoAlvo": publicoAlvo,
            }
            return render(request, 'add_projeto.html', contexto)
        
        try:
            Projeto.objects.create(ong=ong_logada, nome_projeto=nome_projeto, descricao=descricao, metodologiasUtilizadas=metodologiasUtilizadas, publicoAlvo=publicoAlvo,
                                   dataDeCriacao=dataDeCriacao)
        finally:
            return redirect(add_dados)

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
def editar_projeto(request, projeto_id):
    usuario = request.user
    erros = {}

    projeto = Projeto.objects.get(pk=projeto_id)

    if request.method == 'POST':
        nome_projeto = request.POST['nome_projeto']
        descricao = request.POST['descricao']
        metodologiasUtilizadas = request.POST['metodologia']
        publicoAlvo = request.POST['publico']
        dataDeCriacao = request.POST['criacao']

        if not nome_projeto or not descricao or not metodologiasUtilizadas or not publicoAlvo or not dataDeCriacao:
            erros["campos"] = "Preencha todos os campos necessários"
        else:
            projeto.nome_projeto = nome_projeto
            projeto.descricao = descricao
            projeto.metodologiasUtilizadas = metodologiasUtilizadas
            projeto.publicoAlvo = publicoAlvo
            projeto.dataDeCriacao = dataDeCriacao
            projeto.save()
            return redirect('visualizar_projetos', projeto_id=projeto.id)

    contexto = {
        "erros": erros,
        "projeto": projeto,
    }

    return render(request, 'editar_projeto.html', contexto)


@login_required
def add_dados(request):
    usuario = request.user
    ong_logada = Ong.objects.get(nome=usuario.first_name)
    projeto = list(ong_logada.projeto_set.all())
    erros = {}
    if request.method == 'POST':
        errado = False
        project = request.POST['projeto']
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        tipo1 = request.POST['tipo1']
        tipo2 = request.POST['tipo2']

        if not descricao or not titulo or tipo1 == "Selecione o tipo de dado" or tipo2 == "Selecione o tipo de dado":
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True
        
        if errado:
                contexto = {
                    "erros": erros,
                    "projetos": projeto,
                    "descricao": descricao,
                    "titulo": titulo,
                    "tipo1": tipo1,
                    "tipo2": tipo2,
                    "tipos1": tipos1,
                    "tipos2": tipos2
                }
                return render(request, "add_dados.html", contexto)
        
        if DadosImpactos.objects.filter(titulo=titulo).exists():
            contexto = {
                "erros": "esse dado ja existe",
                "projetos": projeto,
                "descricao": descricao,
                "titulo": titulo,
                "tipo1": tipo1,
                "tipo2": tipo2,
                "tipos1": tipos1,
                "tipos2": tipos2
            }
            return render(request, 'add_dados.html', contexto)
        DadosImpactos.objects.create(projeto=Projeto.objects.get(nome_projeto=project),titulo=titulo,descricao=descricao,tipo1=tipo1,tipo2=tipo2)
        dado = DadosImpactos.objects.get(titulo=titulo)
        return redirect(home)
    return render(request,'add_dados.html',{"tipos1": tipos1, "tipos2": tipos2, "projetos": projeto})


@login_required
def editar_dado(request, dado_impacto_id):
    usuario = request.user
    erros = {}

    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)

    if request.method == 'POST':
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        tipo1 = request.POST['tipo1']
        tipo2 = request.POST['tipo2']

        if not titulo or not descricao or tipo1 == "Selecione o tipo de dado" or tipo2 == "Selecione o tipo de dado":
            erros["campos"] = "Preencha todos os campos necessários"
        else:
            dado_impacto.titulo = titulo
            dado_impacto.descricao = descricao
            dado_impacto.tipo1 = tipo1
            dado_impacto.tipo2 = tipo2
            dado_impacto.save()
            return redirect(visualizar_projetos)

    contexto = {
        "erros": erros,
        "dado_impacto": dado_impacto,
        "tipos1": tipos1,
        "tipos2": tipos2,
    }

    return render(request, 'editar_dado.html', contexto)


@login_required
def add_linhas(request, dado_impacto_id):
    usuario = request.user
    erros = {}
    
    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)

    if request.method == 'POST':
        errado = False
        valor1 = request.POST['valor1']
        valor2 = request.POST['valor2']

        if not valor1 or not valor2:
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True
        
        if errado:
                contexto = {
                    "erros": erros,
                    "valor1": valor1,
                    "valor2":valor1,
                }
                return render(request, "add_linhas.html", contexto)
        
        try:
            LinhasImpacto.objects.create(dado_impacto=dado_impacto, valor1=valor1, valor2=valor2)
        finally:
            return redirect('detalhes_dado', dado_impacto_id=dado_impacto_id)
        
    contexto = {
    "erros": erros,
    "dado_impacto": dado_impacto
    }
    
    return render(request,'add_linhas.html', contexto)


@login_required
def editar_linha_impacto(request, linha_impacto_id):
    usuario = request.user
    erros = {}

    linha_impacto = LinhasImpacto.objects.get(pk=linha_impacto_id)
    valor1 = linha_impacto.valor1
    
    if request.method == 'POST':
        errado = False
        valor1_input = request.POST['valor1']
        valor2 = request.POST['valor2']

        valor1_input = float(str(valor1_input).replace(',', '.'))
        
        if not valor1_input or not valor2:
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True
        else:
            valor1 = valor1_input 


        if errado:
            contexto = {
                "erros": erros,
                "valor1": valor1,
                "valor2": valor2,
                "linha_impacto": linha_impacto,
            }
            return render(request, "editar_linha_impacto.html", contexto)

        linha_impacto.valor1 = valor1
        linha_impacto.valor2 = valor2
        linha_impacto.save()

        return redirect('detalhes_dado', dado_impacto_id=linha_impacto.dado_impacto.id)

    contexto = {
        "erros": erros,
        "linha_impacto": linha_impacto,
        "valor1": valor1,
        "valor2": linha_impacto.valor2, 
    }

    return render(request, 'editar_linha_impacto.html', contexto)

@login_required
def visualizar_projetos(request):
    projetos = Projeto.objects.all()
    context = {'projetos': projetos}
    return render(request, 'visualizar_projetos.html', context)   


@login_required
def visualizar_linhas_impacto(request, dado_impacto_id):
    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)
    linhas_impacto = LinhasImpacto.objects.filter(dado_impacto=dado_impacto)
    
    context = {
        'dado_impacto': dado_impacto,
        'linhas_impacto': linhas_impacto,
    }
    
    return render(request, 'detalhes_dado.html', context)
    
