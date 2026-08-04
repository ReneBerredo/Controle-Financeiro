from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Receita, Despesa
from .forms import ReceitaForm, DespesaForm

@login_required
def lista_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user)
    return render(request, 'financas/lista_receitas.html', {'receitas': receitas})

@login_required
def lista_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'financas/lista_despesas.html', {'despesas': despesas})

@login_required
def criar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()

    return render(request, 'financas/criar_receita.html', {'form': form})

@login_required
def criar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            return redirect('lista_despesas')
    else:
        form = DespesaForm()

    return render(request, 'financas/criar_despesa.html', {'form': form})


