import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.contrib.auth.views import LoginView
import requests

def api_get_garages():
    response = requests.get(os.environ.get('API_HOST', 'http://0.0.0.0:') + os.environ.get('API_PORT', '8001') + '/api/garages/')
    response.raise_for_status()
    garages_data = response.json() 
    choices = [(garage['id'], garage['nom']) for garage in garages_data]
    return choices

class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length = 200, 
        label="", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter votre username'
        })    
    )
    email = forms.CharField(
        max_length = 200, 
        label="", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter votre email'
        })    
    )
    password = forms.CharField(
        max_length = 200, 
        label="", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter votre password'
        })    
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']



class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label = "",
        widget=forms.TextInput(attrs={
            "autofocus": True,
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label = "",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'placeholder': 'Password'
        }),
    )


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm


class VoitureSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(VoitureSelectForm, self).__init__(*args, **kwargs)
        try:
            choices = api_get_garages()
        except requests.RequestException as e:
            choices = []
        
        self.fields['garage'] = forms.ChoiceField(
            choices=[("", "Selectionner un garage")]+choices,
            label="",
            required=True
        )


class VoitureAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(VoitureAddForm, self).__init__(*args, **kwargs)
        try:
            choices = api_get_garages()
        except requests.RequestException as e:
            choices = []
        
        self.fields['garage'] = forms.ChoiceField(
            choices=[("", "Selectionner un garage")]+choices,
            label="",
            required=True
        )

        self.fields['couleur']  = forms.CharField(
            max_length = 200, 
            label="", 
            widget = forms.TextInput(attrs={
                'placeholder': 'Entrer la couleur'
            })    
        )

        self.fields['immatriculation']  = forms.CharField(
            max_length = 200, 
            label="", 
            widget = forms.TextInput(attrs={
                'placeholder': 'Entrer l\'immatriculation'
            })    
        )

        self.fields['marque']  = forms.CharField(
            max_length = 200, 
            label="", 
            widget = forms.TextInput(attrs={
                'placeholder': 'Entrer la marque'
            })    
        )

        self.fields['modele']  = forms.CharField(
            max_length = 200, 
            label="", 
            widget = forms.TextInput(attrs={
                'placeholder': 'Entrer le modele'
            })    
        )




class GarageAddForm(forms.Form):
    name = forms.CharField(
        max_length = 200, 
        label="", 
        widget = forms.TextInput(attrs={
            'placeholder': 'Entrer le nom'
        })    
    )


class GarageEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GarageEditForm, self).__init__(*args, **kwargs)
        try:
            choices = api_get_garages()
        except requests.RequestException as e:
            choices = []
        
        self.fields['garage'] = forms.ChoiceField(
            choices=[("", "Selectionner un garage")]+choices,
            label="",
            required=True
        )

        self.fields['name'] = forms.CharField(
            max_length = 200, 
            label="", 
            widget = forms.TextInput(attrs={
                'placeholder': 'Entrer le nom'
            })    
        )
    
  

class GarageDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GarageDeleteForm, self).__init__(*args, **kwargs)
        try:
            choices = api_get_garages()
        except requests.RequestException as e:
            choices = []
        
        self.fields['garage'] = forms.ChoiceField(
            choices=[("", "Selectionner un garage")]+choices,
            label="",
            required=True
        )
