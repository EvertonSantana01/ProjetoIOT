
from django.db import models
from django.utils import timezone

class Consulta(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    ano = models.CharField(max_length=10, blank=True, null=True)
    municipio = models.CharField(max_length=50, blank=True, null=True)
    situacao = models.CharField(max_length=100, blank=True, null=True)
    restricao = models.BooleanField(default=False)
    data_consulta = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.placa} - {self.data_consulta.strftime('%d/%m/%Y %H:%M')}"
