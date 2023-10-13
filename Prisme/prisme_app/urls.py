from django.urls import path, include
from . import views

urlpatterns =[
    path("", views.home, name="home"),
    path("ex", views.teste, name="exemplo")

]