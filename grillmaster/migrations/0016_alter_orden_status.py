# Generated by Django 5.0.6 on 2024-06-24 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grillmaster', '0015_alter_detalles_orden_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='status',
            field=models.IntegerField(default=3),
        ),
    ]