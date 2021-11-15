from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()

choices = (('Full name', 'Full name'),
           ('Email', 'Email'),
           ('Phone number', 'Phone number'),
           ('Text', 'Text'),
           ('Integer', 'Integer'),
           ('Address', 'Address'),
           ('Date', 'Date')
           )

min_validator = MinLengthValidator(1)


class SchemaTable(models.Model):
    title = models.CharField(max_length=20, validators=[min_validator])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modification_date = models.DateTimeField(auto_now_add=True, blank=True)
    column_separator = models.CharField(max_length=2, default=',')
    string_character = models.CharField(max_length=2, default='"')

    class Meta:
        ordering = ['title']


class SchemaField(models.Model):
    name = models.CharField(max_length=20, validators=[min_validator])
    type = models.CharField(max_length=20, choices=choices)
    range_lower = models.IntegerField(default=0)
    range_upper = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    schema_table = models.ForeignKey(SchemaTable, related_name='items', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('schema_table', 'order'),
                           ('schema_table', 'name')]


class SchemaData(models.Model):
    schema_table = models.ForeignKey(SchemaTable, related_name='dataset', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    generated = models.BooleanField(default=False)
    rows = models.IntegerField()
