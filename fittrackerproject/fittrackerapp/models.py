from django.conf import settings
from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL)
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, default=0)
    public = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    rank_in_program = models.IntegerField(default=0)
    number_of_set = models.IntegerField()
    label_data = models.CharField(max_length=50)
    indication = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=0)
    program = models.ManyToManyField(Program, through='Exercise_Program')
    def __str__(self):
        return self.name


class Exercise_Program(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('exercise', 'program')


class Training(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    validated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'program', 'user')


class Data(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    rank_in_set = models.IntegerField()
    value = models.IntegerField()