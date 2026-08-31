from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Receita, Despesa
from .forms import ReceitaForm, DespesaForm
from django.shortcuts import get_object_or_404
import uuid
from dateutil.relativedelta import relativedelta

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
            parcelado = form.cleaned_data['parcelado']
            total_parcelas = form.cleaned_data['total_parcelas']

            if parcelado and total_parcelas:
                grupo = uuid.uuid4()
                data_primeira_parcela = form.cleaned_data['data']

                for numero in range(1, total_parcelas + 1 ):
                    data_parcela = data_primeira_parcela + relativedelta(months=numero - 1)

                    Despesa.objects.create(
                        usuario=request.user,
                        tipo=form.cleaned_data['tipo'],
                        valor=form.cleaned_data['valor'],
                        descricao=form.cleaned_data['descricao'],
                        data=data_parcela,
                        parcelado=True,
                        parcela_atual=numero,
                        total_parcelas=total_parcelas,
                        grupo_parcelamento=grupo,
                    )
            else:
                despesa = form.save(commit=False)
                despesa.usuario = request.user
                despesa.save()

            return redirect('lista_despesas')
    else:
        form = DespesaForm()

    return render(request, 'financas/criar_despesa.html', {'form': form})

@login_required
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id, usuario=request.user)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(instance=receita)

    return render(request, 'financas/editar_receita.html', {'form': form})

@login_required
def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id, usuario=request.user)

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa)

    return render(request, 'financas/editar_despesa.html', {'form': form})

@login_required
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id, usuario=request.user)

    if request.method == 'POST':
        receita.delete()
        return redirect('lista_receitas')

    return render(request, 'financas/excluir_receita.html', {'receita': receita})

@login_required
def excluir_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id, usuario=request.user)

    if request.method == 'POST':
        despesa.delete()
        return redirect('lista_despesas')

    return render(request, 'financas/excluir_despesa.html', {'despesa': despesa})

@login_required
def dashboard(request):
    receitas = Receita.objects.filter(usuario=request.user)
    despesas = Despesa.objects.filter(usuario=request.user)

    total_receitas = receitas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    receitas_por_tipo = receitas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total')
    despesas_por_tipo = despesas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total')

    contexto = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'receitas_por_tipo': receitas_por_tipo,
        'despesas_por_tipo': despesas_por_tipo,
    }

    return render(request, 'financas/dashboard.html', contexto)
