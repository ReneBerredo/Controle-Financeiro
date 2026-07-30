from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Receita, Despesa

@login_required
def lista_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user)
    return render(request, 'financas/lista_receitas.html', {'receitas': receitas})

@login_required
def lista_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'financas/lista_despesas.html', {'despesas': despesas})



