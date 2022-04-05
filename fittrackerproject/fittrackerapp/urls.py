from django.urls import include, path
from . import views
from django.contrib.auth.forms import UserCreationForm

from .models import *
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('register', views.register_view, name = "register"),
    path('login', views.login_view, name = "login"),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard_view, name = "dashboard"),
    path('training/<int:id>', views.training_view, name = "training"),
    path('training_list/<int:id>', views.training_list_view, name = "training_list"),
    path('program/<int:id>', views.program_view, name = "training"),
    path('exercise/<int:id>', views.exercise_view, name = "exercise"),
    path('exercise', views.create_exercise_view, name = "exercise"),
    path('exercise_details/<int:id>', views.exercise_details_view, name = "exercise_details"),
    path('program', views.create_program_view, name = "program"),
    path('library', views.library_view, name="library"),
]