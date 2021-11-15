from django.urls import path
from api import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'api'
urlpatterns = [
    path('schema/', views.SchemaList.as_view(), name="schema_list"),
    path('user/<int:user>/', views.UserSchemas.as_view()),
    path('schema/create/', views.CategorySchema.as_view(), name="schema_create"),
    path('schema/delete/', views.SchemaDelete.as_view(), name="schema_delete"),
    path('schema/<int:pk>/', views.SchemaDetail.as_view(), name="schema_view"),
    path('schema/<int:pk>/edit/', views.SchemaDetail.as_view(), name="schema_edit"),
    path('schema/<int:pk>/data/', views.SchemaDataAPI.as_view(), name="schema_data"),
    path('schema-data/<int:pk>/delete/', views.SchemaDataDelete.as_view(), name="schema_data_delete"),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
