# Generated by Django 3.2.8 on 2021-10-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20211029_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemafield',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
