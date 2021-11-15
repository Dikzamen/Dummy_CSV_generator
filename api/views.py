from api.models import SchemaTable, SchemaField, SchemaData
from api.serializers import SchemaSerializer, SchemaDataSerializer
from django.utils.timezone import now
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from frontend.tasks import create_func, generate_data
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class SchemaList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = SchemaTable.objects.all()
    serializer_class = SchemaSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserSchemas(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView
                  ):
    queryset = SchemaTable.objects.all()
    lookup_field = 'user_id'
    serializer_class = SchemaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategorySchema(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView
                     ):
    queryset = SchemaTable.objects.all()
    serializer_class = SchemaSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user', None)
        if user_id is None:
            return JsonResponse({'user': 'You are not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=request.data['user'])
        serializer = SchemaSerializer(data=request.data)
        errors = {}
        if serializer.is_valid() is False:
            errors.update(serializer.errors)
        if not request.data.get('items', tuple()):
            errors.update({'items': 'No values inside item'})
        if errors:
            return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        item_data = request.data.pop('items')
        request.data.pop('user')
        schema = SchemaTable.objects.create(user=user, **request.data)
        for item in item_data:
            try:
                SchemaField.objects.create(schema_table=schema, **item)
            except IntegrityError as error:
                return JsonResponse({'item': error.args}, status=status.HTTP_400_BAD_REQUEST)
        request.data['id'] = schema.id
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SchemaDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = SchemaTable.objects.all()
    serializer_class = SchemaSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        serializer = SchemaSerializer(data=request.data)
        schema = SchemaTable.objects.get(id=kwargs['pk'])
        errors = {}
        if serializer.is_valid() is False:
            errors.update(serializer.errors)

        if not request.data.get('items', tuple()):
            errors.update({'items': 'No values inside item'})
        if errors:
            return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

        order_set = {d['order'] for d in request.data['items']}
        name_set = {d['name'] for d in request.data['items']}
        if not (len(request.data['items']) == len(order_set) == len(name_set)):
            return JsonResponse({'item': 'Order and name values must be UNIQUE'}, status=status.HTTP_400_BAD_REQUEST)
        schema.modification_date = now()
        schema.title = request.data['title']
        schema.column_separator = request.data['column_separator']
        schema.string_character = request.data['string_character']
        item_data = request.data.pop('items')
        schema.items.all().delete()
        for item in item_data:
            SchemaField.objects.create(schema_table=schema, **item)
        schema.save()
        return Response(serializer.data)


class SchemaDataAPI(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView
                    ):
    queryset = SchemaData.objects.all()
    serializer_class = SchemaDataSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        schema = SchemaTable.objects.get(pk=kwargs['pk'])
        try:
            rows = int(request.data['rows'])
        except ValueError:
            return JsonResponse({'rows': 'Rows should be integer greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)
        if rows < 0:
            return JsonResponse({'rows': 'Rows should be integer greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)

        dataset = SchemaData.objects.create(schema_table=schema, **request.data)
        file_id = dataset.id
        items = sorted(schema.items.all(), key=lambda a: a.order)
        func_lst = create_func(items)
        headers = [item.name for item in items]
        delimiter = schema.column_separator
        quotechar = schema.string_character
        generate_data(file_id, rows, headers, func_lst, delimiter, quotechar)
        dataset.generated = True
        dataset.save()
        serializer = SchemaDataSerializer(dataset)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


def download_csv(request, pk):
    data = SchemaData.objects.get(pk=pk)
    if data is not None:
        return HttpResponse('yes')
    return HttpResponse('no')


class SchemaDelete(mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = SchemaTable.objects.all()
    serializer_class = SchemaSerializer
    authentication_classes = []

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        schema = SchemaTable.objects.get(id=request.data['id'])
        if schema is not None:
            schema.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'id': "Schema doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


class SchemaDataDelete(mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = SchemaData.objects.all()
    serializer_class = SchemaDataSerializer
    authentication_classes = []

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        schema = SchemaData.objects.get(id=kwargs['pk'])
        if schema is not None:
            schema.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'id': "Schema doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
