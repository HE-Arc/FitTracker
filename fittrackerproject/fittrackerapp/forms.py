from dataclasses import field
from pyexpat import model
from django import forms
from .models import Exercise,Program

class ExerciceForm(forms.ModelForm):  
    class Meta:
        model=Exercise
        fields=['name','category','number_of_set','label_data','indication','program',]
        labels = {
        'name': 'Nom',
        'category': 'Catégorie',
        'number_of_set': 'Nombre de série',
        'label_data': 'Etiquette',
        'indication': 'Indication',
        'program': 'Programme',
        }
        widgets={
           'name': forms.TextInput(attrs={'class':'form-control',}),
           'category': forms.Select(attrs={'class':'form-control',}),
           'number_of_set': forms.NumberInput(attrs={'class':'form-control',}),
           'label_data': forms.TextInput(attrs={'class':'form-control',}),
           'indication': forms.TextInput(attrs={'class':'form-control',}),
           'program': forms.Select(attrs={'class':'form-control',}),
        }
        
        
        
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
        