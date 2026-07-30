from django.contrib import admin
from .models import TipoReceita, TipoDespesa, Receita, Despesa

admin.site.register(TipoReceita)
admin.site.register(TipoDespesa)

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'tipo', 'usuario')
    list_filter = ('tipo', 'usuario', 'data')
    search_fields = ('descricao',)

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_filter = ('descricao', 'valor', 'data', 'tipo', 'usuario')
    list_filter = ('tipo', 'usuario', 'data')
    search_fields  = ('descricao',)