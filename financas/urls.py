from django.urls import path
from . import views

urlpatterns = [
    path('receitas/', views.lista_receitas, name='lista_receitas'),
    path('despesas/', views.lista_despesas, name='lista_despesas')
]