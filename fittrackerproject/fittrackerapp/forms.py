from dataclasses import field
from django.forms import ModelForm
from .models import Exercise

class GeneratorForm(ModelForm):
    class Meta:
        model=Exercise
        fields=['name','category','number_of_set','rank_in_program','label_data','indication','program',]
        