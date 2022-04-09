from django import forms
from fittrackerapp.models import *
from collections import UserDict
from dataclasses import field
from pyexpat import model
from urllib import request
from django import forms
from .models import Exercise, Program
from django.contrib.auth.models import User


class ExerciseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label')
        number_of_set = kwargs.pop('number_of_set')

        super(ExerciseForm, self).__init__(*args, **kwargs)

        for i in range(number_of_set):
            self.fields['input' +
                        str(i)] = forms.IntegerField(required=True, label=label)
            self.fields['input' +
                        str(i)].widget.attrs.update({'class': 'form-control form'})

    def save(self, exercise_id, current_training):
        data = self.cleaned_data
        counter = 0

        for k, v in data.items():
            saving = Data(rank_in_set=counter, value=v,
                          exercise_id=exercise_id, training_id=current_training)
            saving.save()
            counter += 1


class CreateExerciseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateExerciseForm, self).__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.filter(owner=user)

    class Meta:
        model = Exercise
        fields = ['name', 'category', 'number_of_set',
                  'label_data', 'indication', 'program']
        name = forms.CharField
        number_of_set = forms.DecimalField
        label_data = forms.CharField
        indication = forms.CharField

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'selected': '1'}),
            'number_of_set': forms.NumberInput(attrs={'class': 'form-control', }),
            'label_data': forms.TextInput(attrs={'class': 'form-control', 'value': 'Poids'}),
            'indication': forms.TextInput(attrs={'class': 'form-control col-xl-4'}),
        }

        labels = {
            'name': 'Nom',
            'category': 'Catégorie',
            'number_of_set': 'Nombre de série',
            'label_data': 'Etiquette',
            'indication': 'Indication',
        }

    program = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label='Programme'
    )


class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ['name', 'discipline', 'public']
        labels = {
            'name': 'Nom',
            'discipline': 'Discipline',
            'owner': 'Utilisateur',
            'public': 'Publique',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'discipline': forms.Select(attrs={'class': 'form-control', }),
            'public': forms.CheckboxInput(attrs={'class': 'form-check-input', }),
        }
