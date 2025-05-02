from django.db import models
from django.utils import timezone

class Consulta(models.Model):
    placa = models.CharField(max_length=10)
    placa_modelo_antigo = models.CharField(max_length=10, blank=True, null=True)
    placa_modelo_novo = models.CharField(max_length=10, blank=True, null=True)
    placa_nova = models.CharField(max_length=1, blank=True, null=True)

    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    submodelo = models.CharField(max_length=100, blank=True, null=True)
    versao = models.CharField(max_length=100, blank=True, null=True)

    ano = models.CharField(max_length=4, blank=True, null=True)
    ano_modelo = models.CharField(max_length=4, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    chassi = models.CharField(max_length=100, blank=True, null=True)
    situacao_chassi = models.CharField(max_length=10, blank=True, null=True)
    situacao_veiculo = models.CharField(max_length=10, blank=True, null=True)
    nacionalidade = models.CharField(max_length=50, blank=True, null=True)

    combustivel = models.CharField(max_length=50, blank=True, null=True)
    potencia = models.CharField(max_length=10, blank=True, null=True)
    cilindradas = models.CharField(max_length=10, blank=True, null=True)

    capacidade_carga = models.CharField(max_length=10, blank=True, null=True)
    quantidade_passageiro = models.CharField(max_length=10, blank=True, null=True)
    peso_bruto_total = models.CharField(max_length=10, blank=True, null=True)
    eixos = models.CharField(max_length=10, blank=True, null=True)

    tipo_veiculo = models.CharField(max_length=50, blank=True, null=True)
    tipo_montagem = models.CharField(max_length=10, blank=True, null=True)

    data_api = models.CharField(max_length=20, blank=True, null=True)
    ultima_atualizacao = models.CharField(max_length=20, blank=True, null=True)

    logo_url = models.URLField(blank=True, null=True)
    restricao1 = models.CharField(max_length=100, blank=True, null=True)
    restricao2 = models.CharField(max_length=100, blank=True, null=True)
    restricao3 = models.CharField(max_length=100, blank=True, null=True)
    restricao4 = models.CharField(max_length=100, blank=True, null=True)

    data_consulta = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.ano})"
