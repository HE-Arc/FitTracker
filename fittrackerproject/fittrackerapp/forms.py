from django import forms
from fittrackerapp.models import *
from collections import UserDict
from dataclasses import field
from pyexpat import model
from urllib import request
from django import forms
from .models import Exercise,Program
from django.contrib.auth.models import User

class ExerciseForm(forms.Form):
    def __init__(self,*args,**kwargs):
        label = kwargs.pop('label')
        number_of_set = kwargs.pop('number_of_set')

        super(ExerciseForm, self).__init__(*args,**kwargs)

        for i in range(number_of_set):
            self.fields['input'+ str(i)] = forms.IntegerField(required=True, label=label)
            self.fields['input'+ str(i)].widget.attrs.update({'class': 'form-control form'})

    def save(self, exercise_id, current_training):
        data = self.cleaned_data
        counter = 0

        for k,v in data.items():
            saving = Data(rank_in_set=counter, value=v, exercise_id=exercise_id, training_id=current_training)
            saving.save()
            counter += 1

class CreateExerciseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateExerciseForm, self).__init__(*args, **kwargs)
        self.fields['program'].queryset=Program.objects.filter(owner=user)

    class Meta:
        model=Exercise
        fields=['name','category','number_of_set','label_data','indication']
        name=forms.CharField
        number_of_set=forms.DecimalField
        label_data=forms.CharField
        indication=forms.CharField

        widgets={
           'name': forms.TextInput(attrs={'class':'form-control',}),
           'category': forms.Select(attrs={'class':'form-control',}),
           'number_of_set': forms.NumberInput(attrs={'class':'form-control',}),
           'label_data': forms.TextInput(attrs={'class':'form-control',}),
           'indication': forms.TextInput(attrs={'class':'form-control',}),
        }

        labels = {
            'name': 'Nom',
            'category': 'Catégorie',
            'number_of_set': 'Nombre de série',
            'label_data': 'Etiquette',
            'indication': 'Indication',
            }

    def save(self, rank):
        if rank is None:
            rank=1
        data = self.cleaned_data
        saving = Exercise(rank_in_program=rank,name=data['name'],number_of_set=data['number_of_set'],category=data['category'],label_data=data['label_data'],indication=data['indication'])
        saving.save()

    program = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label='Programme'
    )

class ProgramForm(forms.ModelForm):
        
    class Meta:
        model=Program
        fields=['name','discipline']
        labels = {
        'name': 'Nom',
        'discipline': 'Discipline',
        'owner': 'Utilisateur',
        }
        widgets={
           'name': forms.TextInput(attrs={'class':'form-control',}),
           'discipline': forms.Select(attrs={'class':'form-control',}),
        }
        

