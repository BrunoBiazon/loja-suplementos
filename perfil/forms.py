from django import forms 
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.PerfilUsuario
        fields = '__all__'
        exclude = ('user',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required= False,
        widget= forms.PasswordInput(),
        label = 'Senha'
    )
    
    password2 = forms.CharField(
        required= False,
        widget= forms.PasswordInput(),
        label = 'Confirme a senha'
    )
    
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2','email')

    def clean(self, *args, **kwargs):
        data = self.data 
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        
        
        if self.user:
            validation_error_msgs['username'] = 'teste logado '
        else:
            validation_error_msgs['username'] = 'teste '
                
        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
        
        return cleaned