# Generated by Django 5.0.6 on 2024-06-11 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grillmaster', '0002_usuarios_delete_users'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='usuarios',
            new_name='Usuario',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='id_user',
            new_name='email',
        ),
    ]
