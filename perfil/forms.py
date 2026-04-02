from django import forms 
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.PerfilUsuario
        fields = '__all__'
        exclude = ('user',)

    def clean(self, *args, **kwargs):
            cleaned = super().clean()
            validation_error_msgs = {}
            
            cpf_data = cleaned.get('cpf')
            
            if cpf_data:
                cpf_db = models.PerfilUsuario.objects.filter(cpf=cpf_data).first()
                
                perfil_id = self.instance.pk 
                if cpf_db:
                    if perfil_id is None or cpf_db.pk != perfil_id:
                        validation_error_msgs['cpf'] = 'Este CPF já está cadastrado em outra conta.'  
                    
            if validation_error_msgs:    
                raise forms.ValidationError(validation_error_msgs)
            
            return cleaned
    
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
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        
        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
        error_msg_user_exists = 'Usuário digitado já existe.'
        error_msg_email_exists = 'Email digitado já existe'        
        error_msg_password_match = 'As senhas não conferem. Digite iguais.'       
        error_msg_password_short = 'Sua senha precisa de pelo menos 8 caracteres.'
        error_msg_required_field = 'Preencha esse campo.'
        
        # user logado - uptade 
        if self.user:
            if usuario_db and usuario_db.id != self.user.id:
                validation_error_msgs['username'] = error_msg_user_exists
            if email_db and email_db.id != self.user.id:
                validation_error_msgs['email'] = error_msg_email_exists
                            
            if password_data or password2_data:
                if not password_data or not password2_data:
                    validation_error_msgs['password'] = error_msg_required_field
                    validation_error_msgs['password2'] = error_msg_required_field
                elif password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
                elif len(password_data) < 8:
                    validation_error_msgs['password'] = error_msg_password_short

        # user deslogado - cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists
            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists
            
            if not password_data or not password2_data:
                validation_error_msgs['password'] = error_msg_required_field
                validation_error_msgs['password2'] = error_msg_required_field
            elif password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match
            elif len(password_data) < 8:
                validation_error_msgs['password'] = error_msg_password_short
                
        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        return cleaned