import re
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from fittrackerapp.models import *
from fittrackerapp.forms import *
from django.template import loader
from django.shortcuts import render
from .forms import CreateExerciseForm,ProgramForm
from .models import Exercise_Program,Exercise
from django.conf import settings
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib import messages



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

@login_required(login_url="login")
def create_exercise_view(request):
    if request.method == "POST":
        form = CreateExerciseForm(request.user.id,data=request.POST)
        rank=Exercise.objects.aggregate(Max('rank_in_program'))
        if form.is_valid():
            form.save(rank['rank_in_program__max'])
            messages.success(request, 'L\'exercice a été créer')
            return redirect('dashboard')
    else:
        form = CreateExerciseForm(request.user.id)
    return render(request,"create_exercise.html",{'form':form})

@login_required(login_url="login")
def create_program_view(request):
    if request.method == "POST":
        form = ProgramForm(data=request.POST)
        if form.is_valid():
            form.save()
            form.instance.owner.add(request.user.id)
            messages.success(request, 'Le programme a été créer')
            return redirect('dashboard')
    else:
        form = ProgramForm()
    return render(request,"create_program.html",{'form':form})


@login_required(login_url="login")
def library_view(request):
    # 1. Afficher les programmes publiques
    program_list = Program.objects.all().filter(public=True).exclude(owner=request.user.id)

    # TODO 2. Pouvoir ajouter un programme à un utilisateur

    if request.method == "POST":
        data = request.POST
        action = data.get('add-program')
        program = Program.objects.filter(id=action)
        # user = request.user
        print(program)
        program.user.add(id=action)

        return HttpResponse(program)

        # program.user_id.add(request.user.id)
        # request.user.program(id=action)


    # return HttpResponse(action)
    # Program_Owner.objects.create(policy=p1, coverage=c2, amount=1)




    return render(request, "library.html", {'program_list': program_list})

    # TODO 3. Si programme déjà présent dans liste de l'utilisateur ne doit pas s'afficher

    # return render(request, "library.html", {'': })

