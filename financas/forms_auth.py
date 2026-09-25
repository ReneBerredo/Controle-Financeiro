from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm


class CadastroForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150)
    last_name = forms.CharField(label='Sobrenome', max_length=150)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'E-mail ou senha incorretos. Verifique e tente novamente.',
        'inactive': 'Esta conta está inativa.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail'
        