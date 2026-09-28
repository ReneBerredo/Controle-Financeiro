from django.db import models
from django.contrib.auth.models import User
import uuid


class TipoReceita(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class TipoDespesa(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class Receita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receitas')
    tipo = models.ForeignKey(TipoReceita, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255, blank=True)
    data = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'

class Despesa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='despesas')
    tipo = models.ForeignKey(TipoDespesa, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255, blank=True)
    data = models.DateField()
    pago = models.BooleanField(default=False)
    parcelado = models.BooleanField(default=False)
    parcela_atual = models.PositiveIntegerField(null=True, blank=True)
    total_parcelas = models.PositiveIntegerField(null=True, blank=True)
    grupo_parcelamento = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'
    
class CategoriaOrcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_orcamento')
    nome = models.CharField(max_length=100)
    percentual_meta = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.nome} ({self.percentual_meta}%)'

class Assinatura(models.Model):
    STATUS_CHOICES = [
        ('trial', 'Período de Teste'),
        ('ativa', 'Ativa'),
        ('expirada', 'Expirada'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assinatura')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='trial')
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField()
    plano = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.usuario.email} - {self.get_status_display()}'
    