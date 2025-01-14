# Generated by Django 5.0.6 on 2024-06-13 04:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grillmaster', '0005_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('nombre', models.CharField(max_length=200)),
                ('id_producto', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=500)),
                ('precio', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('imagen', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('email', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(8)])),
            ],
        ),
    ]
