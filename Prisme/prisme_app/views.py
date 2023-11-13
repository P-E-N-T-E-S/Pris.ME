import pandas as pd
import statistics as sts
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .utils import linhas, barras, criador_senha_aleatoria
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *


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

areaAtuacao = [
"Esportes",
"Direitos Humanos",
"Educação",
"Saúde",
"Cultura e Arte",
"Meio Ambiente",
"Desenvolvimento Comunitário",
"Ajuda Humanitária",
"Empreendedorismo Social",
"Alívio da Pobreza",
"Alimentação e segurança alimentar",
"Causa animal",
"Desenvolvimento internacional",
"Outro",]

def Login(request):
    if request.user != None:
        redirect(home)
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(home_admin)
            else:
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
            moda_impacto = sts.mode(impactados)
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


def home_admin(request):
    return render(request, "admin.html")

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
        
        try:
            Projeto.objects.create(ong=ong_logada, nome_projeto=nome_projeto, descricao=descricao, metodologiasUtilizadas=metodologiasUtilizadas, publicoAlvo=publicoAlvo,
                                   dataDeCriacao=dataDeCriacao)
            Categoria.objects.create(ong=ong_logada, nome=nome_projeto, tipo="Gasto")
        finally:
            return redirect(visualizar_projetos)

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
            return redirect(visualizar_projetos)

    contexto = {
        "erros": erros,
        "projeto": projeto,
    }

    return render(request, 'editar_projeto.html', contexto)


@login_required
def add_dados(request, projeto_id):
    usuario = request.user
    projeto = Projeto.objects.get(pk=projeto_id)
    ong_logada = Ong.objects.get(nome=usuario.first_name)
    erros = {}
    
    if request.method == 'POST':
        errado = False
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        tipo1 = request.POST['tipo1']
        tipo2 = request.POST['tipo2']

        if not descricao or not titulo or tipo1 == "Selecione o tipo de dado Numérico" or tipo2 == "Selecione o tipo de dado Categorico":
            erros["campos"] = "Preencha todos os campos necessários"
            errado = True
        
        if errado:
                contexto = {
                    "erros": erros,
                    "descricao": descricao,
                    "titulo": titulo,
                    "tipo1": tipo1,
                    "tipo2": tipo2,
                    "tipos1": tipos1,
                    "tipos2": tipos2,
                    "projeto": projeto,
                }
                return render(request, "add_dados.html", contexto)
        
        DadosImpactos.objects.create(projeto=projeto,titulo=titulo,descricao=descricao,tipo1=tipo1,tipo2=tipo2)
        return redirect(visualizar_projetos)
    return render(request,'add_dados.html',{"tipos1": tipos1, "tipos2": tipos2})


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

        return render(request, 'detalhes_dado.html', dado_impacto_id=linha_impacto.dado_impacto.id)

    contexto = {
        "erros": erros,
        "linha_impacto": linha_impacto,
        "valor1": valor1,
        "valor2": linha_impacto.valor2, 
    }

    return render(request, 'editar_linha_impacto.html', contexto)


@login_required
def visualizar_projetos(request):
    usuario = request.user
    ong_logada = Ong.objects.get(email=usuario.username)
    projetos = list(ong_logada.projeto_set.all())
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
    
@login_required
def editar_estilo(request):
    navcor = request.POST.get("navcor")
    sidecor = request.POST.get("sidecor")
    backcor = request.POST.get("backcor")
    perfil = request.POST.get("perfil")

    context = {
        'navcor' : navcor,
        'sidecor' : sidecor,
        'backcor' : backcor,
        'perfil' : perfil,
    }

    return render(request, 'editar_estilo.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cadastrar_ong(request):
    context = { 'areaAtuacao': areaAtuacao}

    if request.method == 'POST':
        nome_ong = request.POST['nome_ong']
        email_ong = request.POST['email_ong']
        area = request.POST['areaAtuacao']
        descricao = request.POST['descricao']
        CEP = request.POST['CEP']
        CNPJ = request.POST['CNPJ']
        dataDeCriacao = request.POST['criacao']
        numeroDeVoluntarios = request.POST['numeroDeVoluntarios']

        ong = Ong(
            nome=nome_ong,
            email=email_ong,
            areaAtuacao=area,
            descricao=descricao,
            CEP=CEP,
            CNPJ=CNPJ,
            dataDeCriacao=dataDeCriacao,
            numeroDeVoluntarios=numeroDeVoluntarios)
        ong.save()
        Categoria.objects.create(ong = ong, nome = "Doações", tipo = "Ganho")
        Categoria.objects.create(ong = ong, nome = "Manutenção", tipo = "Gasto")
        Categoria.objects.create(ong = ong, nome = "Pessoal", tipo = "Gasto")

        return redirect(home_admin)
    else:
        return render(request, 'cadastrar_ong.html', context=context)

def controle_de_gastos(request, dado):
    usuario = request.user
    ong = Ong.objects.get(nome=usuario.first_name)
    categoria = ong.categoria_set.get(nome=dado)
    todas = ong.categoria_set.all()
    categorias = [item.nome for item in todas if item.tipo == "Gasto"]
    separador={
        "nome": categoria.nome,
        "linhas": list(categoria.linhacaixa_set.all())
    }
    contexto={
        "caixa": separador,
        "categorias": categorias
    }
    return render(request, "controle_gastos.html", contexto)

def controle_de_ganhos(request, dado):
    usuario = request.user
    ong = Ong.objects.get(nome=usuario.first_name)
    categoria = ong.categoria_set.get(nome=dado)
    todas = ong.categoria_set.all()
    categorias = [item.nome for item in todas if item.tipo == "Ganho"]
    separador={
        "nome": categoria.nome,
        "linhas": list(categoria.linhacaixa_set.all())
    }
    contexto={
        "caixa": separador,
        "categorias": categorias
    }
    return render(request, "controle_ganhos.html", contexto)


def gerar_relatorio(request):
    usuario = request.user
    graficos = []
    titulos = []
    contexto = {}

    ong = Ong.objects.get(nome=usuario.first_name)
    projetos = ong.projeto_set.all()
    for projeto in list(projetos):
        dados = projeto.dadosimpactos_set.all()
        for dado in list(dados):
            linha = dado.linhasimpacto_set.all().values()
            if len(list(linha)) != 0:
                base = pd.DataFrame(linha)
                grafico = linhas(base["valor2"], base["valor1"], dado.titulo, dado.tipo2, dado.tipo1)
                graficos.append(grafico)
                titulos.append(f"{projeto.nome_projeto} - {dado.titulo}")
    contexto["titulos"] = titulos
    if request.method == 'POST':
        texto = request.POST['texto']
        imagem = request.POST['imagem']
        request['relatorio'] = {'texto': texto, 'imagem': imagem}

    return render(request, "preencher_relatorio.html", contexto)


def render_pdf_view(request):
    template_path = 'teste-pdf.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response