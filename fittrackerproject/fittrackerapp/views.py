from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

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