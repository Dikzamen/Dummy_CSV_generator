from rest_framework import serializers
from api.models import SchemaTable, SchemaField, SchemaData


class SchemaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaField
        fields = ['name', 'type', 'range_lower', 'range_upper', 'order']


class SchemaSerializer(serializers.ModelSerializer):
    items = SchemaDetailsSerializer(many=True)

    class Meta:
        model = SchemaTable
        fields = ['title', 'modification_date', 'id',
                  'column_separator', 'string_character', 'items'
                  ]


class SchemaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaData
        fields = ['schema_table', 'date_created', 'generated', 'rows', 'id']
