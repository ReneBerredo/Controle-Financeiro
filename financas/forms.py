from django import forms
from .models import Receita, Despesa

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['tipo', 'valor', 'descricao', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

class DespesaForm(forms.ModelForm):
    parcelado = forms.BooleanField(required=False, label="Despesa parcelada/recorrente?")
    total_parcelas = forms.IntegerField(required=False, min_value=2, label='Quantidade de parcelas')

    class Meta:
        model = Despesa
        fields = ['tipo', 'valor', 'descricao', 'data']
        widgets = {
                    'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
                }
       