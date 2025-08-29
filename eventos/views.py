from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Evento, Lugar 
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import EventoForm, EventoUpdateForm
from django.shortcuts import render
from django.http import JsonResponse

class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.
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
    success_url = reverse_lazy('eventos:evento_list')
    


@method_decorator(staff_member_required, name="dispatch")
class EventoUpdate(UpdateView):
    model = Evento
    form_class =EventoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        # Redirige a la URL de la ficha individual, usando el pk y el slug del objeto.
        return reverse_lazy('eventos:evento_detail', args=[self.object.pk]) + '?ok'
    


@method_decorator(staff_member_required, name="dispatch")   
class EventoDelete(DeleteView):
    model = Evento
    success_url = reverse_lazy('eventos:evento_list')

# Esta es la vista que el calendario usará para obtener los datos.
def lista_eventos_api(request):
    """
    Función para obtener todos los eventos y devolverlos como un JSON.
    """
    eventos = Evento.objects.all().values('id', 'titulo', 'fecha')
    return JsonResponse(list(eventos), safe=False)

# Esta es la que renderiza la plantilla.
def calendario(request):
    """
    Función que renderiza la plantilla calendario.html
    """
    return render(request, 'eventos/calendario.html')