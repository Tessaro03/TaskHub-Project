# Generated by Django 4.2.4 on 2023-08-01 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import usuarios.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=100)),
                ('sobrenome', models.CharField(default='', max_length=100)),
                ('empresa', models.CharField(default='', max_length=100)),
                ('avatar', models.ImageField(blank=True, default='', upload_to=usuarios.models.upload_to)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('enviado', 'Enviado'), ('aceito', 'Aceito'), ('recusado', 'Recusado')], max_length=8)),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='usuarios.userprofile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='usuarios.userprofile')),
            ],
        ),
    ]
