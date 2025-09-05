from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Evento, Lugar 
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import EventoForm, EventoUpdateForm
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

# Create your views here.
class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

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


@method_decorator(staff_member_required, name="dispatch")
class EventoCreate(CreateView):
    model = Evento
    form_class =EventoForm

    def get_success_url(self):
        # Redirige al listado de eventos con '?ok' para indicar que se creó correctamente
        return reverse_lazy('eventos:evento_list') + '?ok'
    


@method_decorator(staff_member_required, name="dispatch")
class EventoUpdate(UpdateView):
    model = Evento
    form_class =EventoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        # Redirige al listado de eventos con un parámetro de consulta 'ok' para indicar éxito
        return reverse_lazy('eventos:evento_list') + '?ok'
        


@method_decorator(staff_member_required, name="dispatch")   
class EventoDelete(DeleteView):
    model = Evento

    def get_success_url(self):
        # Redirige al listado de eventos con '?ok' para indicar que se eliminó correctamente
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