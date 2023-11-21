# Generated by Django 4.2.5 on 2023-11-21 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prisme_app', '0021_alter_editarestilo_sidecor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voluntariado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('nascimento', models.DateField()),
                ('ingresso', models.DateField()),
                ('contato', models.CharField(max_length=50)),
                ('horas', models.IntegerField()),
                ('genero', models.CharField(choices=[(None, 'Selecione seu gênero'), ('Feminino', 'Feminino'), ('Masculino', 'Masculino'), ('Outro', 'Outro')], default=(None, 'Selecione seu gênero'), max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]