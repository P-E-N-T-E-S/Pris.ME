from django.db import models

# Create your models here.

class Ong(models.Model):
     areaAtuação = [
        (None, "Selecione a área de atuação"),
        ("Esportes","Esportes"),
        ("Direitos Humanos","Direitos Humanos"),
        ("Educação","Educação"),
        ("Saúde","Saúde"),
        ("Cultura e Arte","Cultura e Arte"),
        ("Meio Ambiente","Meio Ambiente"),
        ("Desenvolvimento Comunitário","Desenvolvimento Comunitário"),
        ("Ajuda Humanitária","Ajuda Humanitária"),
        ("Empreendedorismo Social","Empreendedorismo Social"),
        ("Alívio da Pobreza","Alívio da Pobreza"),
            ]
     nome = models.CharField(max_length=100)
     areaAtuação = models.CharField(choices=areaAtuação,default=areaAtuação[0],max_length=50)
     descricao = models.TextField(max_length=500, default="Descrição da Ong.")
     CEP = models.CharField(max_length=9)
     CNPJ = models.CharField(max_length=14)
     dataDeCriacao = models.DateField()
     numeroDeVoluntarios = models.PositiveSmallIntegerField()

     def __str__(self):
        return (self.Ong)

class Projeto(models.Model):
    ong = models.ForeignKey(Ong, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500, default="Descrição do Projeto.")
    metodologiasUtilizadas = models.TextField(max_length=500, default="Descreva as metodologias utilizadas.")
    publicoAlvo = models.CharField(max_length=200)
    dataDeCriacao = models.DateField()
    def __str__(self):
        return (self.Projeto)

class DadosImpactos(models.Model):
     projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
     tipo = [
        (None, "Selecione o tipo de dado"),
        ("Pessoas Impactadas por tempo","Pessoas Impactadas por tempo"),
        ("Casas Construidas por tempo","Casas Construidas por tempo"),
        ("Números de Impacto","Números de Impacto"),
        ("Valor por Pessoa","Valor por Pessoa"),
            ]
     titulo = models.CharField(max_length=200)
     descricao = models.CharField(max_length=500)
     valor1 = models.DecimalField(max_digits=10, decimal_places=2)
     valor2 = models.DecimalField(max_digits=10, decimal_places=2) #o valor 2 sempre é CATEGORICO
     tipo = models.CharField(choices=tipo,default=tipo[0],max_length=50)

     def __str__(self):
        return (self.DadosImpactos)
     
     