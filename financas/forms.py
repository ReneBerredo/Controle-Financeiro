from django import forms
from .models import Receita, Despesa

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['tipo', 'valor', 'descricao', 'data']

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['tipo', 'valor', 'descricao', 'data']
        