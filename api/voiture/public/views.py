import json
import os
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .forms import GarageAddForm, GarageDeleteForm, GarageEditForm, UserForm, VoitureAddForm, VoitureSelectForm
import requests
from django.contrib import messages
from django.forms.models import model_to_dict

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def get_profile(userId):
    response = requests.get(os.environ.get('API_HOST', 'http://0.0.0.0:')  + os.environ.get('API_PORT', '8001') + f'/api/profile/{userId}/')
    response.raise_for_status()
    profile_data = response.json() 
    return profile_data[0]



@login_required
def home(request):
    return render(request, "home.html")

@login_required
def profile(request):
    profile = get_profile(request.user.id)        
    return render(request, "profile.html",{'profile': profile})

@login_required
def cle(request):
    return render(request, "cle.html")


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password']) 
            user_data = model_to_dict(user, fields=['id', 'username', 'email','password'])  # Add fields as needed
            url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+('/api/users/add/') 
            requests.post(url, json=user_data)
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user) 
                return redirect('/') 

            return redirect('/')  
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def garage(request):

    if request.method == 'POST':
    
        if "form_add" in request.POST:
            form_add = GarageAddForm(request.POST or None)
            if form_add.is_valid() :
                data = {'nom': form_add.cleaned_data['name']}
                url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+('/api/garages/add/')
                requests.post(url, json=data)
                messages.success(request, "Ajouté avec succès!", extra_tags="form_add")
                print(messages)
    
        elif  "form_edit" in request.POST:
            form_edit = GarageEditForm(request.POST or None)
            if form_edit.is_valid():
                data = {'nom': form_edit.cleaned_data['name']}
                garage = form_edit.cleaned_data['garage']
                url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+(f'/api/garages/{garage}/edit/')
                requests.put(url, json=data)
                messages.success(request, "Modifié avec succès!", extra_tags="form_edit")

        elif "form_delete" in request.POST:
            form_delete = GarageDeleteForm(request.POST or None)
            if form_delete.is_valid() :
                garage = form_delete.cleaned_data['garage']
                url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+(f'/api/garages/{garage}/delete/')
                requests.delete(url)
                messages.success(request, "Supprimé avec succès!",extra_tags="form_delete")
    
    form_add = GarageAddForm()
    form_edit = GarageEditForm()
    form_delete = GarageDeleteForm()

    forms = {
        'form_add': form_add, 
        'form_edit': form_edit, 
        'form_delete': form_delete,
    }
    return render(request, 'garage.html', forms)

@login_required
def voiture(request):
    voitures = []

    if request.method == 'POST':
    
        if "form_select" in request.POST:
            form_select = VoitureSelectForm(request.POST or None)
            if form_select.is_valid() :
                garage = form_select.cleaned_data['garage']
                url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+(f'/api/voitures/{garage}/')
                response = requests.get(url)
                voitures = response.json() 
                print(voitures)
                if response.status_code != 200 : 
                    messages.error(request, "Aucune voiture dans ce garage!", extra_tags="form_select")

        elif  "form_add" in request.POST:
            form_add = VoitureAddForm(request.POST or None)
            if form_add.is_valid() :
                data = form_add.cleaned_data
                data["garage"] = data["garage"]
                url = os.environ.get('API_HOST', 'http://0.0.0.0:')+os.environ.get('API_PORT', '8001')+(f'/api/voitures/add/')
                response = requests.post(url, json=data)
                messages.success(request, "Ajouté avec succès!", extra_tags="form_add")

    form_select = VoitureSelectForm()
    form_add = VoitureAddForm()
    forms = {'form_select': form_select, 'form_add' : form_add ,'voitures': voitures}
    return render(request, 'voiture.html',forms )


### debug 



def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")
