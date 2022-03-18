import re
from django.shortcuts import render, redirect

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from fittrackerapp.models import *
from fittrackerapp.forms import *


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = UserCreationForm(request.POST)
        if form.is_valid():  # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.save()  # Log the user in
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "register.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
        else:
            return redirect('dashboard')
    else:
        form = AuthenticationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "login.html", {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')


@login_required(login_url="login")
def dashboard_view(request):
    program_list = Program.objects.filter(owner=request.user.id)

    return render(request, "dashboard.html", {'program_list': program_list})


@login_required(login_url="login")
def training_view(request, id):
    exercises_list = Exercise.objects.filter(exercise_program__program_id=id)
    request.session['program_id'] = id
    if 'dashboard' in request.META['HTTP_REFERER']:
        request.session['first'] = 1
    return render(request, "training_index.html", {'exercises_list': exercises_list})


@login_required(login_url="login")
def exercise_view(request, id):
    if request.method == "POST":
        exercise = Exercise.objects.get(exercise_program__exercise_id=id)
        # Pass information from form with request.POST
        form = ExerciseForm(request.POST, label="Poids",
                            number_of_set=exercise.number_of_set)
        if form.is_valid():
            if request.session['first'] == 1:
                training = Training(program_id=request.session['program_id'])
                training.save()
                request.session['first'] = 0
                request.session['training_id'] = training.id

            exercise = form.save(exercise.id, request.session['training_id'])
        return redirect('/training/' + str(request.session['program_id']))
    else:
        exercise = Exercise.objects.get(exercise_program__exercise_id=id)
        form = ExerciseForm(label=exercise.label_data,
                            number_of_set=exercise.number_of_set)
        return render(request, "exercise.html", {'exercise': exercise, 'form': form})
