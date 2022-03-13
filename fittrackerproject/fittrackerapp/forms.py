from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import Exercise,Program

class ExerciceForm(ModelForm):
    class Meta:
        model=Exercise
        fields=['name','category','number_of_set','rank_in_program','label_data','indication','program',]
        labels = {
        'name': 'Nom',
        'category': 'Catégorie',
        'number_of_set': 'Nombre de série',
        'rank_in_program': 'Nombre de répétitions',
        'label_data': 'Label_data',
        'indication': 'Indication',
        'program': 'Programme',
        }
        
        
class ProgramForm(ModelForm):
    class Meta:
        model=Program
        fields=['name','discipline']
        labels = {
        'name': 'Nom',
        'discipline': 'Discipline',
        }
        