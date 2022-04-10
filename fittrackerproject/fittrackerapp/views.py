import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from fittrackerapp.models import *
from fittrackerapp.forms import *
from django.template import loader
from django.shortcuts import render
from .forms import CreateExerciseForm, ProgramForm, AuthenticationForm, UserCreationForm
from .models import Exercise_Program, Exercise
from django.conf import settings
from django.db.models import Max
from django.core.exceptions import PermissionDenied


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def message_view(request):
    return render(request, "message_error.html")


def register_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = UserCreationForm(data=request.POST)
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
            return redirect('dashboard')
    else:
        form = AuthenticationForm()  # Create a new instance of this form
        # Send the UserCreationForm to render
    return render(request, "login.html", {'form': form})


@login_required(login_url="login")
def exercise_details_view(request, program_id, exercise_id):
    check_program = Program.objects.filter(
        owner=request.user.id, id=program_id).exists()
    check_exercise = Exercise.objects.filter(
        exercise_program__program_id=program_id, id=exercise_id).exists()
    if check_program:
        if check_exercise:
            exercises_list = Exercise.objects.filter(
                exercise_program__program_id=program_id)
            exercise = Exercise.objects.filter(
                exercise_program__exercise_id=exercise_id).first()
            training_list = Training.objects.filter(
                user_id=request.user.id, program_id=program_id, validated=True)
            data = []
            [data.append(Data.objects.filter(exercise_id=exercise_id,
                         training_id=training.id)) for training in training_list]
            zipped_data = zip(training_list, data)
            return render(request, "exercise_details.html", {'exercise': exercise, 'training_list': training_list, 'data': data, 'exercises_list': exercises_list, 'program_id': program_id, 'zipped_data': zipped_data})
        else:
            raise PermissionDenied("Erreur : Aucune donnée correspondante")
    else:
        raise PermissionDenied("Erreur : Aucune donnée correspondante")


@login_required(login_url="login")
def training_list_view(request, program_id):
    check_program = Program.objects.filter(
        owner=request.user.id, id=program_id).exists()
    if check_program:
        exercises_list = Exercise.objects.filter(
            exercise_program__program_id=program_id)
        return render(request, "training_list.html", {'exercises_list': exercises_list, 'program_id': program_id})
    else:
        raise PermissionDenied("Erreur : Aucune donnée correspondante")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')


@login_required(login_url="login")
def dashboard_view(request):
    program_list = Program.objects.filter(owner=request.user.id)
    count_training = Training.objects.filter(user_id=request.user.id).count()
    last_training = Training.objects.filter(user_id=request.user.id).last()
    training_list = Program.objects.filter(owner=request.user.id)
    datas_list = zip(program_list, training_list)
    return render(request, "dashboard.html", {'datas_list': datas_list, 'count_training': count_training, 'last_training': last_training})


@login_required(login_url="login")
def program_view(request, id):
    if request.method == "POST":
        if 'training_id' not in request.session:
            return redirect('dashboard')
        else:
            Training.objects.filter(
                id=request.session['training_id']).update(validated=True)
            del request.session['training_id']
            return redirect('dashboard')
    else:
        exercises_list = Exercise.objects.filter(
            exercise_program__program_id=id)
        request.session['program_id'] = id

        if 'training_id' not in request.session:
            is_done = []
        else:
            print(f"training id : {request.session['training_id']}")
            is_done = [Data.objects.filter(training_id=request.session['training_id'], exercise_id=exercise.id).first()
                       for exercise in exercises_list]
            if len(is_done) != 0:
                is_done = [i.exercise_id for i in is_done if i is not None]

        referer = request.META.get('HTTP_REFERER')
        if referer is None:
            # request.session['first'] = 1
            pass
        else:
            if 'dashboard' in request.META['HTTP_REFERER']:
                request.session['first'] = 1

        return render(request, "training_index.html", {'exercises_list': exercises_list, 'is_done': is_done})


@login_required(login_url="login")
def exercise_view(request, id):
    if request.method == "POST":
        exercise = Exercise.objects.filter(
            exercise_program__exercise_id=id).first()
        # Pass information from form with request.POST
        form = ExerciseForm(request.POST, label="Poids",
                            number_of_set=exercise.number_of_set)
        if form.is_valid():
            if request.session['first'] == 1:
                training = Training(
                    program_id=request.session['program_id'], user_id=request.user.id)
                training.save()
                request.session['first'] = 0
                request.session['training_id'] = training.id

            exercise = form.save(exercise.id, request.session['training_id'])
        return redirect('/program/' + str(request.session['program_id']))
    else:
        if 'training_id' in request.session:
            already_done = Data.objects.filter(
                training_id=request.session['training_id'], exercise_id=id).first()
            if already_done != None:
                return redirect('/program/' + str(request.session['program_id']))
        exercise = Exercise.objects.filter(
            exercise_program__exercise_id=id).first()
        if exercise == None:
            raise PermissionDenied("Vous n'avez pas accès à cette page")
        form = ExerciseForm(label=exercise.label_data,
                            number_of_set=exercise.number_of_set)
        return render(request, "exercise.html", {'exercise': exercise, 'form': form})


@login_required(login_url="login")
def create_exercise_view(request):
    if request.method == "POST":
        form = CreateExerciseForm(request.user.id, data=request.POST)
        rank = Exercise.objects.aggregate(Max('rank_in_program'))
        if rank['rank_in_program__max'] is None:
            rank['rank_in_program__max'] = 1
        if form.is_valid():
            form.instance.rank_in_program = rank['rank_in_program__max']+1
            form.save()
            return redirect('dashboard')
    else:
        form = CreateExerciseForm(request.user.id)
    return render(request, "create_exercise.html", {'form': form})


@login_required(login_url="login")
def create_program_view(request):
    if request.method == "POST":
        form = ProgramForm(data=request.POST)
        if form.is_valid():
            form.save()
            form.instance.owner.add(request.user.id)
            return redirect('dashboard')
    else:
        form = ProgramForm()
    return render(request, "create_program.html", {'form': form})


@login_required(login_url="login")
def library_view(request):
    # Show public program
    program_list = Program.objects.all().filter(
        public=True).exclude(owner=request.user.id)
    user = request.user

    if request.method == "POST":
        data = request.POST
        action = data.get('add-program')
        program = Program.objects.filter(id=action).get()
        program.owner.add(user)
    owner_list = Program.objects.filter(owner=user.id, public=False)
    shared_list = Program.objects.filter(owner=user.id, public=True)

    return render(request, "library.html", {'program_list': program_list, 'owner_list': owner_list, 'shared_list': shared_list})


@login_required(login_url="login")
def training_view(request, id):
    program_list = Program.objects.filter(owner=request.user.id)
    count_training = Training.objects.filter(user_id=request.user.id).count()
    last_training = Training.objects.filter(user_id=request.user.id).last()
    return render(request, "dashboard.html", {'program_list': program_list, 'count_training': count_training, 'last_training': last_training})
