from django import forms
from django.db.models import Q
from .models import Receita, Despesa, TipoReceita, TipoDespesa

class ReceitaForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(queryset=None, label='Tipo de Receita')

    class Meta:
        model = Receita
        fields = ['tipo', 'valor', 'descricao', 'data', 'pago']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoReceita.objects.filter(Q(usuario__isnull=True) | Q(usuario=usuario))

class DespesaForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(queryset=None, label='Tipo de Despesa')
    parcelado = forms.BooleanField(required=False, label='Despesa parcelada/recorrente?')
    total_parcelas = forms.IntegerField(required=False, min_value=2, label='Quantidade de parcelas')

    class Meta:
        model = Despesa
        fields = ['tipo', 'valor', 'descricao', 'data', 'pago']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoDespesa.objects.filter(Q(usuario__isnull=True) | Q(usuario=usuario))

    def clean(self):
        cleaned_data = super().clean()
        parcelado = cleaned_data.get('parcelado')
        total_parcelas = cleaned_data.get('total_parcelas')

        if parcelado and not total_parcelas:
            raise forms.ValidationError('Informe a quantidade de parcelas para uma despesa parcelada.')

        return cleaned_data

class TipoReceitaForm(forms.ModelForm):
    class Meta:
        model = TipoReceita
        fields = ['nome']

class TipoDespesaForm(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        fields = ['nome']
        