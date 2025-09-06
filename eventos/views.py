from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Evento, Lugar 
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import EventoForm, EventoUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import AccessMixin

# Create your views here.

class OwnerOrSuperuserRequiredMixin(AccessMixin):
    """
    Mixin que comprueba si el usuario es un superusuario o el creador del objeto.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Obtiene el objeto para verificar la propiedad
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

        # Comprueba si el usuario es superusuario o el creador del objeto
        if not (request.user.is_superuser or obj.creador == request.user):
            # Redirige a una página de acceso denegado o a la lista de eventos
            return redirect('eventos:evento_list')
            
        return super().dispatch(request, *args, **kwargs)

class EventoListView(ListView):
    """
    Vista para mostrar una lista de todos los eventos.
    """
    model = Evento
    paginate_by = 8 # Número de eventos por página

class EventoDetailView(DetailView):
    """
    Vista para mostrar los detalles de un solo evento.
    """
    model = Evento

    
class EventoCreate(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'


class EventoUpdate(OwnerOrSuperuserRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'
        

class EventoDelete(OwnerOrSuperuserRequiredMixin, DeleteView):
    model = Evento
    
    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'

# Vista de la API para el calendario
class EventoApiView(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        
        eventos_formateados = []
        for evento in eventos:
            eventos_formateados.append({
                'title': evento.titulo,
                # Usamos .isoformat() para formatear las fechas y horas correctamente
                'start': f"{evento.fecha.isoformat()}T{evento.hora_inicio.isoformat()}",
                'end': f"{evento.fecha.isoformat()}T{evento.hora_fin.isoformat()}",
                'url': reverse('eventos:evento_detail', args=[evento.pk])
            })
        
        return JsonResponse(eventos_formateados, safe=False)

# Vista para el calendario (renderiza la plantilla)
class CalendarioView(TemplateView):
    template_name = 'eventos/calendario.html'