# Generated by Django 4.2.5 on 2023-10-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("prisme_app", "0007_remove_ong_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dadosimpactos",
            name="tipo",
        ),
        migrations.AddField(
            model_name="dadosimpactos",
            name="tipo1",
            field=models.CharField(
                choices=[
                    (None, "Selecione o tipo de dado"),
                    ("Pessoas Impactadas", "Pessoas Impactadas"),
                    ("Casas Contruidas", "Casas Contruidas"),
                    ("Numérica", "Numérica"),
                    ("Valor", "Valor"),
                ],
                default=(None, "Selecione o tipo de dado"),
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="dadosimpactos",
            name="tipo2",
            field=models.CharField(
                choices=[
                    (None, "Selecione o tipo de dado"),
                    ("Tempo", "Tempo"),
                    ("Categorico", "Categorico"),
                    ("Pessoa", "Pessoa"),
                ],
                default=(None, "Selecione o tipo de dado"),
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="dadosimpactos",
            name="valor2",
            field=models.CharField(max_length=20),
        ),
    ]
