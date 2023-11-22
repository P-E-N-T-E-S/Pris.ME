import pandas as pd
import statistics as sts
import os
import csv
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .utils import linhas, barras, criador_senha_aleatoria, validar_cep, validar_cnpj
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.core.mail import send_mail


tipos1 = [
    "Selecione o tipo de dado Numérico",
    "Pessoas Impactadas",
    "Casas Contruidas",
    "Árvores plantadas",
    "Lixo removido (TON)",
    "Médicos alocados",
    "Alunos ajudados",
    "Merendas Disponibilizadas",
    "Tratamentos Disponibilizadas",
    "Animais ajudados",
]

tipos2 = [
    "Selecione o tipo de dado Categorico",
    "Tempo",
    "Pessoas",
    "Km2",
    "Bairro",
    "Estado",
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
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect(home_admin)
        else:
            return redirect(home)
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            if not user.is_staff:
                return redirect(home)
            else:
                return redirect(home_admin)
        else:
            return render(request, "login.html", {"erro": "Usuário não encontrado."})
    return render(request, "login.html")


@login_required
def home(request):
    moda = True
    usuario = request.user
    graficos = []
    impactados = []
    contexto = {}
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto["sidecor"] = layout.sidecor
    contexto["backcor"] = layout.backcor

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


@login_required
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
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}
    
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
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }
    return render(request, 'add_projeto.html', contexto)


@login_required
def editar_projeto(request, projeto_id):
    usuario = request.user
    erros = {}
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}

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
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }

    return render(request, 'editar_projeto.html', contexto)


@login_required
def add_dados(request, projeto_id):
    usuario = request.user
    projeto = Projeto.objects.get(pk=projeto_id)
    ong_logada = Ong.objects.get(nome=usuario.first_name)
    erros = {}
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}
    
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
    return render(request,'add_dados.html',{"tipos1": tipos1, "tipos2": tipos2, "sidecor": layout.sidecor, "backcor": layout.backcor})


@login_required
def editar_dado(request, dado_impacto_id):
    usuario = request.user
    layout = EditarEstilo.objects.get(user_id=usuario)
    erros = {}
    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)
    print(layout)
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
        "sidecor": layout.sidecor, 
        "backcor": layout.backcor
    }

    return render(request, 'editar_dado.html', contexto)


@login_required
def add_linhas(request, dado_impacto_id):
    usuario = request.user
    erros = {}
    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}


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
    "dado_impacto": dado_impacto,
    "sidecor": layout.sidecor, "backcor": layout.backcor
    }
    
    return render(request,'add_linhas.html', contexto)


@login_required
def editar_linha_impacto(request, linha_impacto_id):
    usuario = request.user
    erros = {}
    linha_impacto = LinhasImpacto.objects.get(pk=linha_impacto_id)
    valor1 = linha_impacto.valor1
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}
    
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
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }

    return render(request, 'editar_linha_impacto.html', contexto)


@login_required
def visualizar_projetos(request):
    usuario = request.user
    context = {}
    layout = EditarEstilo.objects.get(user_id=usuario)
    ong_logada = Ong.objects.get(email=usuario.username)
    projetos = list(ong_logada.projeto_set.all())
    context = {'projetos': projetos, "sidecor": layout.sidecor, "backcor": layout.backcor}
    return render(request, 'visualizar_projetos.html', context)   


@login_required
def visualizar_linhas_impacto(request, dado_impacto_id):
    usuario = request.user
    layout = EditarEstilo.objects.get(user_id=usuario)
    dado_impacto = DadosImpactos.objects.get(pk=dado_impacto_id)
    linhas_impacto = LinhasImpacto.objects.filter(dado_impacto=dado_impacto)
    
    context = {
        'dado_impacto': dado_impacto,
        'linhas_impacto': linhas_impacto,
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }
    
    return render(request, 'detalhes_dado.html', context)
    
    
@login_required
def editar_estilo(request):
    usuario = request.user
    context = {}
    layout = EditarEstilo.objects.get(user_id=usuario)
    context["sidecor"] = layout.sidecor
    context["backcor"] = layout.backcor
    
    if request.method == 'POST':
        layout = EditarEstilo.objects.get(user_id=usuario)
        layout.sidecor = request.POST.get("sidecor")
        layout.backcor = request.POST.get("backcor")

        layout.save()
        
        context = {
            'sidecor' : layout.sidecor,
            'backcor' : layout.backcor,
        }

    return render(request, 'editar_estilo.html', context)

@login_required
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

@login_required
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

@login_required
def render_pdf_view(request):
    template_path = 'teste-pdf.html'
    context = {'myvar': request.session['relatorio']['texto'], 'grafico': request.session['relatorio']['graficos'][request.session['relatorio']['index']]}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def gerar_relatorio(request):
    usuario = request.user
    graficos = []
    titulos = []
    contexto = {}
    indice = 0

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
                titulos.append({'titulo': f"{projeto.nome_projeto} - {dado.titulo}",
                                'index': indice})
                indice+=1
    contexto["titulos"] = titulos
    if request.method == 'POST':
        texto = request.POST['texto']
        graph = int(request.POST['grafindex'])
        request.session['relatorio'] = {'texto': texto, 'graficos': graficos, "index": graph}
        return redirect(render_pdf_view)

    return render(request, "preencher_relatorio.html", contexto)


@login_required
def voluntariado(request):
    usuario = request.user
    layout = EditarEstilo.objects.get(user_id=usuario)
    
    voluntarios = list(usuario.voluntariado_set.all())
    contexto = {
        "voluntarios": voluntarios,
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }
    return render(request, "voluntariado.html", contexto)


@login_required
def add_voluntario(request):
    usuario = request.user
    layout = EditarEstilo.objects.get(user_id=usuario)
    contexto = {}
    
    nome = ''
    nascimento = ''
    ingresso = ''
    contato = ''
    horas = ''
    genero = ''
    
    if request.method == 'POST':
        nome = request.POST['nome']
        nascimento = request.POST['nascimento']
        ingresso = request.POST['ingresso']
        contato = request.POST['contato']
        horas = request.POST['horas']
        genero = request.POST['genero']

        
        try:
            Voluntariado.objects.create(nome=nome, nascimento=nascimento, ingresso=ingresso, contato=contato, horas=horas,
                                   genero=genero)
        finally:
            return redirect(voluntariado)

    contexto = {
        "nome": nome,
        "nascimento": nascimento,
        "ingresso": ingresso,
        "contato": contato,
        "horas": horas,
        "genero": genero,
        "generos": genero,
        "sidecor": layout.sidecor, "backcor": layout.backcor
    }
    return render(request, "add_voluntario.html", contexto)

@login_required
def editar_voluntario(request):
    return render(request, "editar_voluntario.html")
    
    
    
    
# Admin
def is_admin(user):
    return not user.groups.filter(name__startswith='OngGroup_').exists()


def Login_Admin(request):
    if request.user != None:
        redirect(home)
    if request.method == "POST":
        user = request.POST["user"]
        senha = request.POST["senha"]
        user = authenticate(request, username=user, password=senha)
        if user is not None and is_admin:
            login(request, user)
            return redirect(home_admin)
        else:
            return render(request, "login_admin.html", {"erro": "Usuário não encontrado."})
    return render(request, "login_admin.html")
    
    
@login_required
@user_passes_test(is_admin)
def home_admin(request):
    contexto = {}
    
    ongs = Ong.objects.all() 
    
    usuario = request.user
    
    layout = EditarEstilo.objects.get(user_id=usuario)

    contexto = {
        'ongs': ongs,
        'sidecor': layout.sidecor,
        'backcor': layout.backcor
    }
    
    return render(request, "home_admin.html", context=contexto)


@login_required
@user_passes_test(is_admin)
def cadastrar_ong(request):
    context = {'areaAtuacao': areaAtuacao}

    if request.method == 'POST':
        errado = False
        erros = {}
        
        nome_ong = request.POST['nome_ong']
        email_ong = request.POST['email_ong']
        area = request.POST['areaAtuacao']
        descricao = request.POST['descricao']
        CEP = request.POST['CEP']
        CNPJ = request.POST['CNPJ']
        dataDeCriacao = request.POST['criacao']
        numeroDeVoluntarios = request.POST['numeroDeVoluntarios']

        if request.method == 'POST':
            send_mail(
                    (f"Bem vindo(a) ao Pris.me, { nome_ong }: !"),
                    (f"Bem vindo(a) ao Pris.me\nSeu login é: { email_ong }\nSua senha é: Senha Inicial"),
                    "suporte.pris.me@gmail.com",
                    [f"{email_ong}"],
                    fail_silently=False,
                )
            

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


@login_required
@user_passes_test(is_admin)
def editar_ong(request, ong_id):
    ong = Ong.objects.get(id=ong_id)
    contexto = {
        "nome": ong.nome,
        "email": ong.email,
        "areaAtuacao": ong.areaAtuacao,
        "descricao": ong.descricao,
        "CEP": ong.CEP,
        "CNPJ": ong.CNPJ,
        "dataDeCriacao": ong.dataDeCriacao,
        "numeroDeVoluntarios": ong.numeroDeVoluntarios,
        'areaAtuacao': areaAtuacao,
        'ong': ong,
    }
    
    if request.method == 'POST':
        ong.nome = request.POST['nome']
        ong.email = request.POST['email']
        ong.areaAtuacao = request.POST['areaAtuacao']
        ong.descricao = request.POST['descricao']
        ong.CEP = request.POST['CEP']
        ong.CNPJ = request.POST['CNPJ']
        ong.dataDeCriacao = request.POST['dataDeCriacao']
        ong.numeroDeVoluntarios = request.POST['numeroDeVoluntarios']
        ong.save()

        return redirect('home_admin')

    return render(request, 'editar_ong.html', context=contexto)


@login_required
@user_passes_test(is_admin)
def deletar_ong(request, ong_id):
    Ong.objects.delete(id=ong_id)
    return redirect(home_admin)


def baixar_impacto(request, projeto):
    usuario = request.user
    ong = Ong.objects.get(nome=usuario.first_name)
    projeto = list(ong.projeto_set.filter(nome_projeto=projeto))
    dados = list(projeto[0].dadosimpactos_set.all())
    contexto = {
        'listdados': [{'nome': dados[i].titulo, 'index': i} for i in range(len(dados))]
    }
    if request.method == "POST":

        index = int(request.POST["dado_impacto"])

        dados = list(projeto[0].dadosimpactos_set.all())
        dado = dados[index]
        lista = [[dado.tipo1, dado.tipo2]]
        linhas = list(dado.linhasimpacto_set.all())
        for linha in linhas:
            lista.append([linha.valor1, linha.valor2])
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment: filename={dado.titulo}.csv"
        csv_writer = csv.writer(response, delimiter=';')
        for linha in lista:
            csv_writer.writerow(linha)
        return response
    return render(request, "baixardados.html", contexto)