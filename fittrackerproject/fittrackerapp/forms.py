from collections import UserDict
from dataclasses import field
from pyexpat import model
from urllib import request
from django import forms
from .models import Exercise,Program
from django.contrib.auth.models import User

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        """ Customises the labels for checkboxes"""
        return "%s" % member.name

class ExerciceForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        super(ExerciceForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Program.objects.filter(
            user=self.request.user)     
             
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
        data = self.cleaned_data
        saving = Exercise(rank_in_program=rank,name=data['name'],number_of_set=data['number_of_set'],category=data['category'],label_data=data['label_data'],indication=data['indication'])
        saving.save() 
           
    program = CustomModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
        
class ProgramForm(forms.ModelForm):
    class Meta:
        model=Program
        fields=['name','discipline']
        labels = {
        'name': 'Nom',
        'discipline': 'Discipline',
        }
        widgets={
           'name': forms.TextInput(attrs={'class':'form-control',}),
           'discipline': forms.Select(attrs={'class':'form-control',}),
        }
        
    def usess(self, rank):
        global user
        user=rank
        