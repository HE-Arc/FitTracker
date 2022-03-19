from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render
from .forms import ExerciseForm,ProgramForm
from .models import Exercise_Program,Exercise
from django.conf import settings
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib import messages

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
def create_exercise_view(request):
    if request.method == "POST":
        form = ExerciseForm(request.user.id,data=request.POST)
        rank=Exercise.objects.aggregate(Max('rank_in_program')).value()[0]
        if form.is_valid():
            form.save(rank)
            messages.success(request, 'L\'exercice a été créer')
            return redirect('home') 
    else:
        form = ExerciseForm(request.user.id)
    return render(request,"exercise.html",{'form':form})

@login_required(login_url="login")
def program_view(request):
    if request.method == "POST":
        form = ProgramForm(data=request.POST) 
        form.save() 
        messages.success(request, 'Le programme a été créer')
        return redirect('home')
    else:
        form = ProgramForm()
    return render(request,"program.html",{'form':form})