from dataclasses import field
from django.forms import ModelForm
from .models import Exercise,Program

class ExerciceForm(ModelForm):
    class Meta:
        model=Exercise
        fields=['name','category','number_of_set','rank_in_program','label_data','indication','program',]
        
class ProgramForm(ModelForm):
    class Meta:
        model=Program
        fields=['name','discipline']
        