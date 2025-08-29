# registration/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save  
from django.dispatch import receiver

# No se necesita el modelo SecurityQuestion porque las preguntas son fijas.

# Modelo de usuario personalizado con dos preguntas de seguridad fijas
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    departamento = models.CharField(max_length=100)
    
    # Las preguntas son fijas, por lo que solo guardamos las respuestas y la etiqueta aquí.
    respuesta_seguridad_1 = models.CharField(
        max_length=255, 
        verbose_name="¿Cuál es el nombre de tu primera mascota?"
    )
    respuesta_seguridad_2 = models.CharField(
        max_length=255, 
        verbose_name="¿Cuál es el nombre de tu abuela materna?"
    )

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()  # Elimina la imagen antigua si existe
    return 'profiles/' + filename

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']

# Signal para crear o actualizar el perfil automáticamente

@receiver(post_save, sender=CustomUser)
def ensure_profile_exists(sender, instance, **kwargs):
        if kwargs.get('created', False):
            # Si el usuario es recién creado, crea un perfil asociado   
            Profile.objects.get_or_create(user=instance)
            

    
