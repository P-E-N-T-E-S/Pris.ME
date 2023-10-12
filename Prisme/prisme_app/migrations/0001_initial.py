# Generated by Django 4.2.5 on 2023-10-12 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('areaAtuação', models.CharField(choices=[(None, 'Selecione a área de atuação'), ('Esportes', 'Esportes'), ('Direitos Humanos', 'Direitos Humanos'), ('Educação', 'Educação'), ('Saúde', 'Saúde'), ('Cultura e Arte', 'Cultura e Arte'), ('Meio Ambiente', 'Meio Ambiente'), ('Desenvolvimento Comunitário', 'Desenvolvimento Comunitário'), ('Ajuda Humanitária', 'Ajuda Humanitária'), ('Empreendedorismo Social', 'Empreendedorismo Social'), ('Alívio da Pobreza', 'Alívio da Pobreza')], default=(None, 'Selecione a área de atuação'), max_length=50)),
                ('descricao', models.TextField(default='Descrição da Ong.', max_length=500)),
                ('CEP', models.CharField(max_length=9)),
                ('CNPJ', models.CharField(max_length=14)),
                ('dataDeCriacao', models.DateField()),
                ('numeroDeVoluntarios', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(default='Descrição do Projeto.', max_length=500)),
                ('metodologiasUtilizadas', models.TextField(default='Descreva as metodologias utilizadas.', max_length=500)),
                ('publicoAlvo', models.CharField(max_length=200)),
                ('dataDeCriacao', models.DateField()),
                ('ong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prisme_app.ong')),
            ],
        ),
        migrations.CreateModel(
            name='DadosImpactos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=500)),
                ('valor1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(choices=[(None, 'Selecione o tipo de dado'), ('Pessoas Impactadas por tempo', 'Pessoas Impactadas por tempo'), ('Casas Construidas por tempo', 'Casas Construidas por tempo'), ('Números de Impacto', 'Números de Impacto'), ('Valor por Pessoa', 'Valor por Pessoa')], default=(None, 'Selecione o tipo de dado'), max_length=50)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prisme_app.projeto')),
            ],
        ),
    ]
