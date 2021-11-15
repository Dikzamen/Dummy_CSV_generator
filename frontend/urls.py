from django.urls import path
from frontend import views

app_name = 'app'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('schemas/', views.schemas, name='schemas'),
    path('schemas/<int:pk>/', views.schema_view, name='schema_view'),
    path('schemas/create/', views.schema_create, name='schema_create'),
    path('schemas/<int:pk>/data/', views.schema_csv, name='schema_data'),
]

