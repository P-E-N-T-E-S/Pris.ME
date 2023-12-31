from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


class Ong(models.Model):
     areaAtuacao = [
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
        ("Alimentação e segurança alimentar","Alimentação e segurança alimentar"),
        ("Causa animal","Causa animal"),
        ("Desenvolvimento internacional","Desenvolvimento internacional"),
        ("Outro","Outro"),
            ]
     nome = models.CharField(max_length=100)
     email = models.EmailField(max_length=100)
     areaAtuacao = models.CharField(choices=areaAtuacao,default=areaAtuacao[0],max_length=50)
     descricao = models.TextField(max_length=500, default="Descrição da Ong.")
     CEP = models.CharField(max_length=9)
     CNPJ = models.CharField(max_length=14)
     dataDeCriacao = models.DateField()
     numeroDeVoluntarios = models.PositiveSmallIntegerField()
    
     def __str__(self):
        return (self.nome)
 
 
@receiver(post_save, sender=Ong)
def create_user_and_group_for_ong(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.email, password='senha_inicial', first_name=instance.nome)
        instance.user = user
        
        group_name = f'OngGroup_{instance.id}'
        ong_group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(ong_group)
        
        instance.save()       
        
        
class Projeto(models.Model):
    ong = models.ForeignKey(Ong, on_delete=models.CASCADE)
    nome_projeto = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500, default="Descrição do Projeto.")
    metodologiasUtilizadas = models.TextField(max_length=500, default="Descreva as metodologias utilizadas.")
    publicoAlvo = models.CharField(max_length=200)
    dataDeCriacao = models.DateField()
    def __str__(self):
        return (self.nome_projeto)

class DadosImpactos(models.Model):
     projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
     tipo2 = [
        (None, "Selecione o tipo de dado"),
         ("Tempo","Tempo"),
         ("Pessoa","Pessoa"),
         ("Km2","Km2"),
         ("Bairro", "Bairro"),
         ("Estado", "Estado")
            ]
     tipo1 = [
         (None, "Selecione o tipo de dado"),
         ("Pessoas Impactadas", "Pessoas Impactadas"),
         ("Casas Contruidas", "Casas Contruidas"),
         ("Árvores plantadas", "Árvores plantadas"),
         ("Lixo removido (TON)", "Lixo removido (TON)"),
         ("Médicos alocados", "Médicos alocados"),
         ("Alunos ajudados", "Alunos ajudados"),
         ("Merendas Disponibilizadas", "Merendas Disponibilizadas"),
         ("Tratamentos Disponibilizadas", "Tratamentos Disponibilizadas"),
         ("Animais ajudados","Animais ajudados")
     ]
     titulo = models.CharField(max_length=200)
     descricao = models.CharField(max_length=500)
     tipo1 = models.CharField(choices=tipo1,default=tipo1[0],max_length=50)
     tipo2 = models.CharField(choices=tipo2, default=tipo2[0], max_length=50)
     def __str__(self):
        return (self.titulo)


class LinhasImpacto(models.Model):
    dado_impacto = models.ForeignKey(DadosImpactos, on_delete=models.CASCADE)
    valor1 = models.DecimalField(max_digits=10, decimal_places=2)
    valor2 = models.CharField(max_length=20)


class Categoria(models.Model):
    escolhas =[("Ganho", "Ganho"), ("Gasto", "Gasto")]
    ong = models.ForeignKey(Ong, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(choices=escolhas, default=escolhas[1], max_length=100)
    def __str__(self):
        return self.nome



class LinhaCaixa(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.IntegerField()
    data = models.DateField()
    identificacao = models.CharField(max_length=100)

    def __str__(self):
        return self.identificacao

class EditarEstilo(models.Model):
    sidecor = models.CharField(max_length=20, default='#FFFFFF')
    backcor = models.CharField(max_length=20, default='#f5f7fa')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
@receiver(post_save, sender=User)
def create_estilo_user(sender, instance, created, **kwargs):
    if created:
        EditarEstilo.objects.create(user=instance)
        

class Voluntariado(models.Model):
    generos = [(None, "Selecione..."), ("Feminino", "Feminino"), ("Masculino", "Masculino"), ("Outro", "Outro")]
    nome = models.CharField(max_length=100)
    nascimento = models.DateField()
    ingresso = models.DateField()
    contato = models.CharField(max_length=50)
    horas = models.CharField(max_length=50)
    genero = models.CharField(choices=generos, default=generos[0], max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
   