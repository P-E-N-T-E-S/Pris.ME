from django.urls import path, include
from . import views

urlpatterns =[
    path("", views.home, name="home"),
    path("ex", views.teste, name="exemplo"),
    path("add_projeto",views.add_projeto, name="add_projeto"),
    path("add_dados",views.add_dados, name="add_dados")

]