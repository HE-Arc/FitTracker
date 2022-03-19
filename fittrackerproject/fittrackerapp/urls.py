from django.urls import include, path
from . import views
from django.contrib.auth.forms import UserCreationForm

from .models import *
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('index', views.index, name = "index"),
    path('register', views.register_view, name = "register"),
    path('login', views.login_view, name = "login"),
    path('logout', views.logout_view, name='logout'),
    path('exercice', views.create_exercise_view, name = "exercice"),
    path('program', views.program_view, name = "program"),
]