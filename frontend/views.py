from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from api.models import SchemaTable, SchemaData
from django.core.exceptions import ObjectDoesNotExist


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(f'USER = {user}')
        if user is not None:
            if user.is_active:
                login(request, user)
            return HttpResponseRedirect(reverse('app:schemas'))
    return render(request, 'frontend/login.html')


@login_required
def schemas(request):
    print(request.user)
    schema_lst = SchemaTable.objects.filter(user=request.user)
    context = {'schemas': schema_lst, 'user': request.user}
    return render(request, 'frontend/schemas.html', context)


@login_required
def edit_schema(request):
    schema_lst = SchemaTable.objects.filter(user=request.user)
    context = {'schemas': schema_lst, 'user': request.user}
    return render(request, 'frontend/new_schema.html', context)


@login_required
def schema_view(request, pk):
    try:
        schema = SchemaTable.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('app:schemas'))
    if schema.user.id != request.user.id:
        return HttpResponseRedirect(reverse('app:schemas'))
    context = {'schema': schema, 'method': 'PUT', 'user': request.user }
    return render(request, 'frontend/new_schema.html', context)


@login_required
def schema_create(request):
    context = {'method': 'POST', 'user': request.user}
    return render(request, 'frontend/new_schema.html', context)


@login_required
def schema_csv(request, pk):
    schema = SchemaTable.objects.get(id=pk)
    datasets = SchemaData.objects.filter(schema_table=schema)
    context = {'schema': schema, 'datasets': datasets}
    return render(request, 'frontend/data_sets.html', context)
