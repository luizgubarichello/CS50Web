from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

from . import validators


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="Seu email.")
    first_name = forms.CharField(
        label='Primeiro Nome',
        max_length=32,
        help_text="Seu primeiro nome. Ex: 'Fulano Beltrano'."
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=32,
        help_text="Seu sobrenome. Ex: 'Silva'."
    )
    cpf = forms.CharField(
        max_length=11,
        label='CPF',
        validators=[validators.validate_cpf],
        help_text="Seu CPF."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'cpf', 'email', 'password1', 'password2']
    