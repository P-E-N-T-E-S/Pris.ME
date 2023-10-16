from django.urls import path, include
from . import views

urlpatterns =[
    path("", views.home, name="home"),
    path("login", views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path("add_projeto",views.add_projeto, name="add_projeto"),
    path("add_dados",views.add_dados, name="add_dados")

]