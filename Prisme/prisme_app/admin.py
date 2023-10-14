from django.contrib import admin
from .models import Projeto,Ong,DadosImpactos
# Register your models here.

admin.site.register(Ong)
admin.site.register(Projeto)
admin.site.register(DadosImpactos)