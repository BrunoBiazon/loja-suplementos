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
        
        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password')
        
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
        error_msg_user_exists = 'Usuário digitado já existe.'
        error_msg_email_exists = 'Email digitado já existe'        
        error_msg_password_match = 'As senhas não conferem. Digite iguais.'       
        error_msg_password_short = 'Sua senha precisa de pelo menos 8 caracteres.'
        error_msg_required_filed = 'Preencha esse campo.'
        
        # user logado - update
        if self.user:
            validation_error_msgs['username'] = 'teste logado '
            
            
        # user deslogado
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists
                
            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists
                
            if password_data != password_data2:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password_confirm'] = error_msg_password_match
            elif len(password_data) < 8:
                validation_error_msgs['password'] = error_msg_password_short    
                
        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
        
        return cleaned