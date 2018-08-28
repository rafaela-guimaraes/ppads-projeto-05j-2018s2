from django.contrib.auth.models import User
from django import forms
from .models import Entry, Category
from django.utils import timezone


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Senha',widget=forms.PasswordInput)
    email = forms.CharField(label='Email')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EntryForm(forms.ModelForm):
    description = forms.CharField(label='Descrição', required=True)
    amount = forms.FloatField(label='Valor', required=True, min_value=0.1)
    entry_date = forms.DateField(label='Data', initial=timezone.now, required=True)

    def __init__(self, *args, **kwargs):
        entry_type = kwargs.pop('entry_type')
        super().__init__(*args, **kwargs)

        self.fields['category'].label = 'Categoria'
        self.fields['category'].queryset = Category.objects.order_by('description').filter(entries_type=entry_type)
    
    class Meta:
        model = Entry
        fields = ['category', 'description', 'amount', 'entry_date']

