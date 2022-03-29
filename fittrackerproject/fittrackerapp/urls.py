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
    path('exercise/<int:id>', views.exercise_view, name = "exercise"),
    path('exercise', views.create_exercise_view, name = "exercise"),
    path('program', views.create_program_view, name = "program"),
    path('library', views.library_view, name="library"),
]