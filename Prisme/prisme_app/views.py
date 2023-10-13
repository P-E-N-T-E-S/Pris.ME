from django.shortcuts import render, redirect
from .utils import linhas, barras
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

# Create your views here.

#@login_required
def home(request):
    contexto = {
    }
    return render(request, "home.html", context=contexto)

#@login_required
def add_di(request):
    contexto = {

    }
    return render(request, "dados.html", context=contexto)

#@login_required
def teste(request):
    contexto={
        "grafico": linhas([1,2,3], [20,30,40], "penis", "penisX", "penisY")
    }
    return render(request, "ex.html", context=contexto)

def login(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return render(request, "login.html", {"erro": "Usuário não encontrado"})
    return render(request, "login.html")
