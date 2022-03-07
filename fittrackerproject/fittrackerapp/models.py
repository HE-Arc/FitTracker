from django.conf import settings
from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Program(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL)
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    rank_in_program = models.IntegerField()
    number_of_set = models.IntegerField()
    label_data = models.CharField(max_length=50)
    indication = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    program = models.ManyToManyField(Program, through='Exercise_Program')


class Exercise_Program(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)


class Training(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)


class Data(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    rank_in_set = models.IntegerField()
    value = models.IntegerField()


# class User_Program(models.Model):
#     user = models.ManyToManyField(settings.AUTH_USER_MODEL)
#     program = models.ManyToManyField(Program)
