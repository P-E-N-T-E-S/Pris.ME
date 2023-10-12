from django.shortcuts import render
from .utils import linhas
# Create your views here.

def home(request):
    contexto = {
    }
    return render(request, "home.html", context=contexto)

def add_di(request):
    contexto = {

    }
    return render(request, "dados.html", context=contexto)