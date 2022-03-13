from django.contrib import admin

from .models import Category, Discipline, Exercise, Program

admin.site.register(Category)
admin.site.register(Exercise)
admin.site.register(Program)
admin.site.register(Discipline)

