from django.urls import path, include
from . import views


urlpatterns =[
    path("", views.Login, name='login'),
    path("home", views.home, name="home"),
    path("login", views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path("add_projeto",views.add_projeto, name="add_projeto"),
    path('add_dados/<int:projeto_id>/', views.add_dados, name='add_dados'),
    path("add_linhas/<str:dado_impacto_id>",views.add_linhas, name="add_linhas"),
    path("visualizar_projetos",views.visualizar_projetos, name="visualizar_projetos"),
    path("editar_linha_impacto/<str:linha_impacto_id>",views.editar_linha_impacto, name="editar_linha_impacto"),
    path("detalhes_dado/<str:dado_impacto_id>",views.visualizar_linhas_impacto, name="detalhes_dado"),
    path('editar_projeto/<int:projeto_id>/', views.editar_projeto, name='editar_projeto'),
    path('editar_dado/<int:dado_impacto_id>/', views.editar_dado, name='editar_dado'),
    path('editar_estilo', views.editar_estilo, name='editar_estilo'),
    path("controle_gastos/<str:dado>", views.controle_de_gastos, name="controle_gastos"),
    path("controle_ganhos/<str:dado>", views.controle_de_ganhos, name="controle_ganhos"),
    path('login_admin', views.Login_Admin, name='login_admin'),
    path('home_admin', views.home_admin, name='home_admin'),
    path('cadastrar_ong', views.cadastrar_ong, name='cadastrar_ong'),
    path("pdf", views.render_pdf_view, name="pdf"),
    path("relatorio", views.gerar_relatorio, name='relatorio'),
    path('editar_ong/<int:ong_id>/', views.editar_ong, name='editar_ong'),
    path('deletar_ong/<int:ong_id>/', views.deletar_ong, name='deletar_ong'),
    ]
