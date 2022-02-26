from django.db import models


class Program(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)


class Discipline(models.Model):
    name = models.CharField(max_length=50)
