from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    nombre_mision = models.CharField(max_length=100)
    descr = models.TextField(max_length=500)
    puntos = models.IntegerField()

    def __str__(self):
        return self.nombre_mision

class Puntos_usuario(models.Model):
    puntos = models.IntegerField(default=0) #Total de puntos acumulados por el usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def sumar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()

class Historial_misiones(models.Model):
    mision = models.ForeignKey(Task, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)