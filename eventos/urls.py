from django.urls import path
from .views import (
    EventoListView, EventoDetailView, EventoCreate, 
    EventoUpdate, EventoDelete
)
from . import views


eventos_patterns = ([
    # Muestra la lista de todos los eventos
    path('', EventoListView.as_view(), name='evento_list'),
    # Muestra los detalles de un evento específico
    path('<int:pk>/', EventoDetailView.as_view(), name='evento_detail'),
    # Crea un nuevo evento
    path('crear/', EventoCreate.as_view(), name='evento_create'),
    # Edita un evento existente
    path('<int:pk>/editar/', EventoUpdate.as_view(), name='evento_update'),
    # Elimina un evento
    path('<int:pk>/eliminar/', EventoDelete.as_view(), name='evento_delete'),
    # API para obtener la lista de eventos en formato JSON
    path('api/eventos/', views.lista_eventos_api, name='lista_eventos_api'),
    
    # Vista para renderizar el calendario
    
    path('calendario/', views.calendario, name='calendario'),
    
], 'eventos')