# registration/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile

# Preguntas de seguridad fijas
PREGUNTA_1 = "¿Cuál es el nombre de tu primera mascota?"
PREGUNTA_2 = "¿Cuál es el nombre de tu abuela materna?"

# Formulario para la creación de un nuevo usuario
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    departamento = forms.CharField(max_length=100, required=True, label="Departamento")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    respuesta_seguridad_1 = forms.CharField(
        max_length=255, 
        required=True, 
        label=PREGUNTA_1
    )
    respuesta_seguridad_2 = forms.CharField(
        max_length=255, 
        required=True, 
        label=PREGUNTA_2
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email',
            'telefono',
            'departamento',
            'respuesta_seguridad_1',
            'respuesta_seguridad_2',
        )

# --- Formularios para la recuperación de contraseña ---

User = get_user_model()

# Paso 1: Formulario para identificar al usuario por nombre de usuario
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario"
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario no existe.')
        return username

# Paso 2: Formulario para las preguntas de seguridad
class SecurityQuestionsForm(forms.Form):
    respuesta_seguridad_1 = forms.CharField(
        max_length=255, 
        label="¿Cuál es el nombre de tu primera mascota?"
    )
    respuesta_seguridad_2 = forms.CharField(
        max_length=255, 
        label="¿Cuál es el nombre de tu abuela materna?"
    )

# Paso 3: Formulario para el perfil del usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 3, 'placeholder': 'Escribe algo sobre ti...'}),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Enlace a tu perfil o sitio web'}),
        }


class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        help_text="Introduce tu nuevo correo electrónico"
    )

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Esta es la validación más segura.
        # Excluimos al usuario actual de la búsqueda de duplicados.
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige uno diferente.")
        
        return email