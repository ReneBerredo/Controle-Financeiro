from django import forms
from .models import Receita, Despesa

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['tipo', 'valor', 'descricao', 'data', 'pago']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

class DespesaForm(forms.ModelForm):
    parcelado = forms.BooleanField(required=False, label="Despesa parcelada/recorrente?")
    total_parcelas = forms.IntegerField(required=False, min_value=2, label='Quantidade de parcelas')

    class Meta:
        model = Despesa
        fields = ['tipo', 'valor', 'descricao', 'data', 'pago']
        widgets = {
                    'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
                }
        
    def clean(self):
        cleaned_data = super().clean()
        parcelado = cleaned_data.get('parcelado')
        total_parcelas = cleaned_data.get('total_parcelas')

        if parcelado and not total_parcelas:
            raise forms.ValidationError('Informa a quantidade de parcelas para uma despesa parcelada.')

        return cleaned_data
    