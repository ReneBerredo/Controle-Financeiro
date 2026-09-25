from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms_auth import LoginForm

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('receitas/', views.lista_receitas, name='lista_receitas'),
    path('receitas/nova/', views.criar_receita, name='criar_receita'),
    path('tipos-receita/nova/', views.criar_tipo_receita, name='criar_tipo_receita'),
    path('tipos-despesa/nova/', views.criar_tipo_despesa, name='criar_tipo_despesa'),
    path('receitas/<int:receita_id>/editar/', views.editar_receita, name='editar_receita'),
    path('receitas/<int:receita_id>/excluir/', views.excluir_receita, name='excluir_receita'),
    path('despesas/', views.lista_despesas, name='lista_despesas'),
    path('despesas/nova/', views.criar_despesa, name='criar_despesa'),
    path('despesas/<int:despesa_id>/editar/', views.editar_despesa, name='editar_despesa'),
    path('despesas/<int:despesa_id>/excluir/', views.excluir_despesa, name='excluir_despesa'),
    path('login/', auth_views.LoginView.as_view(template_name='financas/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('receitas/<int:receita_id>/alternar-pago/', views.alternar_pago_receita, name='alternar_pago_receita'),
    path('despesas/<int:despesa_id>/alternar-pago/', views.alternar_pago_despesa, name='alternar_pago_despesa'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('esqueci-senha/', auth_views.PasswordResetView.as_view(template_name='financas/senha_reset.html'), name='password_reset'),
    path('esqueci-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='financas/senha_reset_enviado.html'), name='password_reset_done'),
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='financas/senha_reset_confirmar.html'), name='password_reset_confirm'),
    path('resetar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='financas/senha_reset_concluido.html'), name='password_reset_complete'),
]
