from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from fittrackerapp.models import *

def index(request):
    return HttpResponse("Hello, world. You're logged  in.")

def home(request):
    return render(request,"home.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST) # Pass information from form with request.POST
        if form.is_valid(): # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.save() # Log the user in
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm() # Create a new instance of this form
    return render(request,"register.html", {'form':form}) # Send the UserCreationForm to render

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST) # Pass information from form with request.POST
        if form.is_valid(): # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
        else:
            return redirect('home')
    else:
        form = AuthenticationForm() # Create a new instance of this form
    return render(request,"login.html", {'form':form}) # Send the UserCreationForm to render

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')

@login_required(login_url="login")
def generator_view(request):
    return HttpResponse("Generator page")

@login_required(login_url="login")
def training_view(request):
    form = 0
    return render(request,"training.html", {'form':form})

@login_required(login_url="login")
def dashboard_view(request):
    program_list = Program.objects.all()
    return render(request,"dashboard.html", {'program_list':program_list})

def training_index_view(request, id):
    exercises_list = Exercise.objects.filter(exercise_program__program_id=id) # TODO
    return render(request,"training_index.html", {'exercises_list': exercises_list})

def exercise_view(request, id):
    exercise = Exercise.objects.get(exercise_program__exercise_id=id)
    return render(request,"exercise.html", {'exercise': exercise})
