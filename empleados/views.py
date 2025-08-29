# empleados/views.py
from django.urls import reverse_lazy
from .models import Empleado, Departamento
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EmpleadoForm, EmpleadoUpdateForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator



class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.
class EmpleadoListView(ListView):
    model = Empleado
    paginate_by = 8 # Número de empleados por página

class EmpleadoDetailView(DetailView):
    model = Empleado

@method_decorator(staff_member_required, name="dispatch")
class EmpleadoCreate(CreateView):
    model = Empleado
    form_class =EmpleadoForm
    success_url = reverse_lazy('empleados:empleados')

@method_decorator(staff_member_required, name="dispatch")
class EmpleadoUpdate(UpdateView):
    model = Empleado
    form_class =EmpleadoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        # Redirige a la URL de la ficha individual, usando el pk y el slug del objeto.
        return reverse_lazy('empleados:empleado', args=[self.object.pk]) + '?ok'
    

@method_decorator(staff_member_required, name="dispatch")   
class EmpleadoDelete(DeleteView):
    model = Empleado
    success_url = reverse_lazy('empleados:empleados')

