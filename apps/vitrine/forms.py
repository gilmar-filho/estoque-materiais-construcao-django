from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.core.models import Usuario


class CadastroClienteForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'telefone',
            'password1',
            'password2',
        ]