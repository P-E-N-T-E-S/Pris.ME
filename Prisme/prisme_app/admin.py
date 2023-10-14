from django.contrib import admin
from .models import Projeto,Ong,DadosImpactos, LinhasImpacto
# Register your models here.

admin.site.register(Ong)
admin.site.register(Projeto)
admin.site.register(DadosImpactos)
admin.site.register(LinhasImpacto)