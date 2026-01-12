from django import forms
from django.contrib.auth.forms import UserCreationForm
from import_export.forms import ImportForm

from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(
        label='É Superusuário?',
        required=False,
        help_text='Marque se este usuário precisa de acesso total e senha.'
    )

    class Meta:
        model = Usuario
        fields = ('cpf', 'nome_completo', 'cr', 'funcao', 'categoria', 'pcd', 'aprendiz', 'data_de_admissao',
                  'data_de_demissao', 'situacao', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if is_superuser:
            if not p1 or not p2:
                raise forms.ValidationError("Senha obrigatória para Superusuários.")
            if p1 != p2:
                raise forms.ValidationError("As senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        is_superuser = self.cleaned_data.get('is_superuser')
        if is_superuser:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
            user.set_unusable_password()

        if commit:
            user.save()
        return user


class CustomImportForm(ImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'input_format' in self.fields:
            del self.fields['input_format']
        if 'resource' in self.fields:
            del self.fields['resource']
