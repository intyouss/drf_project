# Generated by Django 4.2.1 on 2023-05-22 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address_address_alter_address_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(default='', max_length=20, verbose_name='区县'),
        ),
    ]
