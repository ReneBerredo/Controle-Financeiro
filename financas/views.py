from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Receita, Despesa
from .forms import ReceitaForm, DespesaForm, TipoReceitaForm, TipoDespesaForm
from django.shortcuts import get_object_or_404
import uuid
import json
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth
from collections import defaultdict
from datetime import datetime

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
        form = ReceitaForm(request.POST, usuario=request.user)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(usuario=request.user)

    return render(request, 'financas/criar_receita.html', {'form': form})


@login_required
def criar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST, usuario=request.user)
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
                        pago=form.cleaned_data['pago'],
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
        form = DespesaForm(usuario=request.user)

    return render(request, 'financas/criar_despesa.html', {'form': form})

@login_required
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id, usuario=request.user)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita, usuario=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(instance=receita, usuario=request.user)

    return render(request, 'financas/editar_receita.html', {'form': form})

@login_required
def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id, usuario=request.user)

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa, usuario=request.user)
        if form.is_valid():
            parcelado = form.cleaned_data['parcelado']
            total_parcelas = form.cleaned_data['total_parcelas']

            if parcelado and total_parcelas and not despesa.parcelado:
                grupo = uuid.uuid4()
                data_primeira_parcela = form.cleaned_data['data']

                despesa.tipo = form.cleaned_data['tipo']
                despesa.valor = form.cleaned_data['valor']
                despesa.descricao = form.cleaned_data['descricao']
                despesa.data = data_primeira_parcela
                despesa.pago = form.cleaned_data['pago']
                despesa.parcelado = True
                despesa.parcela_atual = 1
                despesa.total_parcelas = total_parcelas
                despesa.grupo_parcelamento = grupo
                despesa.save()

                for numero in range(2, total_parcelas + 1):
                    data_parcela = data_primeira_parcela + relativedelta(months=numero - 1)

                    Despesa.objects.create(
                        usuario=request.user,
                        tipo=form.cleaned_data['tipo'],
                        valor=form.cleaned_data['valor'],
                        descricao=form.cleaned_data['descricao'],
                        data=data_parcela,
                        pago=form.cleaned_data['pago'],
                        parcelado=True,
                        parcela_atual=numero,
                        total_parcelas=total_parcelas,
                        grupo_parcelamento=grupo,
                    )
            else:
                form.save()

            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa, usuario=request.user)

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

def preparar_dados_grafico(queryset, total):
    labels = []
    valores = []
    itens = []

    for item in queryset:
        nome = item['tipo__nome']
        valor = float(item['total'])
        percentual = round((valor / float(total)) * 100, 1) if total > 0 else 0

        labels.append(nome)
        valores.append(valor)
        itens.append({'nome': nome, 'valor': valor, 'percentual': percentual})

    return labels, valores, itens

@login_required
def dashboard(request):
    receitas = Receita.objects.filter(usuario=request.user)
    despesas = Despesa.objects.filter(usuario=request.user)

    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        receitas = receitas.filter(data__gte=data_inicial)
        despesas = despesas.filter(data__gte=data_inicial)

    if data_final:
        receitas = receitas.filter(data__lte=data_final)
        despesas = despesas.filter(data__lte=data_final)

    total_receitas = receitas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    receitas_recebidas = receitas.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    receitas_a_receber = receitas.filter(pago=False).aggregate(Sum('valor'))['valor__sum'] or 0

    despesas_pagas = despesas.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    despesas_a_pagar = despesas.filter(pago=False).aggregate(Sum('valor'))['valor__sum'] or 0

    receitas_por_tipo = receitas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total')
    despesas_por_tipo = despesas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total')

    receitas_grafico_labels, receitas_grafico_valores, receitas_itens = preparar_dados_grafico(receitas_por_tipo, total_receitas)
    despesas_grafico_labels, despesas_grafico_valores, despesas_itens = preparar_dados_grafico(despesas_por_tipo, total_despesas)

    evolucao_receitas = (
        receitas
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    evolucao_despesas = (
        despesas
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    dados_por_mes = defaultdict(lambda: {'receitas': 0, 'despesas': 0})

    for item in evolucao_receitas:
        chave = item['mes'].strftime('%Y-%m')
        dados_por_mes[chave]['receitas'] = float(item['total'])

    for item in evolucao_despesas:
        chave = item['mes'].strftime('%Y-%m')
        dados_por_mes[chave]['despesas'] = float(item['total'])

    meses_ordenados = sorted(dados_por_mes.keys())

    evolucao_labels = [datetime.strptime(m, '%Y-%m').strftime('%b/%Y') for m in meses_ordenados]
    evolucao_receitas_valores = [dados_por_mes[m]['receitas'] for m in meses_ordenados]
    evolucao_despesas_valores = [dados_por_mes[m]['despesas'] for m in meses_ordenados]

    contexto = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'receitas_por_tipo': receitas_por_tipo,
        'despesas_por_tipo': despesas_por_tipo,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'receitas_recebidas': receitas_recebidas,
        'receitas_a_receber': receitas_a_receber,
        'despesas_pagas': despesas_pagas,
        'despesas_a_pagar': despesas_a_pagar,
        'evolucao_labels': evolucao_labels,
        'evolucao_receitas_valores': evolucao_receitas_valores,
        'evolucao_despesas_valores': evolucao_despesas_valores,
        'receitas_grafico_labels': receitas_grafico_labels,
        'receitas_grafico_valores': receitas_grafico_valores,
        'receitas_itens': receitas_itens,
        'despesas_grafico_labels': despesas_grafico_labels,
        'despesas_grafico_valores': despesas_grafico_valores,
        'despesas_itens': despesas_itens,
    }

    return render(request, 'financas/dashboard.html', contexto)

@login_required
def alternar_pago_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id, usuario=request.user)
    receita.pago = not receita.pago
    receita.save()
    return redirect('lista_receitas')

@login_required
def alternar_pago_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id, usuario=request.user)
    despesa.pago = not despesa.pago
    despesa.save()
    return redirect('lista_despesas')

@login_required
def criar_tipo_receita(request):
    if request.method == 'POST':
        form = TipoReceitaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.usuario = request.user
            tipo.save()
            return redirect('criar_receita')
    else:
        form = TipoReceitaForm()

    return render(request, 'financas/criar_tipo_receita.html', {'form': form})

@login_required
def criar_tipo_despesa(request):
    if request.method == 'POST':
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.usuario = request.user
            tipo.save()
            return redirect('criar_despesa')
    else:
        form = TipoDespesaForm()

    return render(request, 'financas/criar_tipo_despesa.html', {'form': form})
