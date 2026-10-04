from django.shortcuts import redirect
from django.urls import reverse
from .models import Assinatura


class ControleAssinaturaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            try:
                assinatura = Assinatura.objects.get(usuario=request.user)
            except Assinatura.DoesNotExist:
                assinatura = None

            if assinatura:
                if assinatura.dias_restantes() == 0 and assinatura.status != 'expirada':
                    assinatura.status = 'expirada'
                    assinatura.save()

                caminhos_permitidos = [
                    reverse('assinatura'),
                    reverse('logout'),
                    reverse('criar_pagamento'),
                    reverse('pagamento_sucesso'),
                    reverse('pagamento_falha'),
                    reverse('webhook_mercadopago'),
                ]

                if assinatura.status == 'expirada' and request.path not in caminhos_permitidos:
                    return redirect('assinatura')

        return self.get_response(request)
    