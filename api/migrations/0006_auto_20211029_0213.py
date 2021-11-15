# Generated by Django 3.2.8 on 2021-10-28 23:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_schemafield_schema_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemafield',
            name='name',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='schematable',
            name='title',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]