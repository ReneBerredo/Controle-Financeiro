from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('receitas/', views.lista_receitas, name='lista_receitas'),
    path('receitas/nova/', views.criar_receita, name='criar_receita'),
    path('despesas/', views.lista_despesas, name='lista_despesas'),
    path('despesas/nova/', views.criar_despesa, name='criar_despesa'),
    path('login/', auth_views.LoginView.as_view(template_name='financas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]