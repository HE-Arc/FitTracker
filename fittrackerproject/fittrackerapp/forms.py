from django import forms
from fittrackerapp.models import *

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

        for index, value in enumerate(data):
            saving = Data(rank_in_set=data['input'+str(index)], value=value, exercise_id=exercise_id, training_id=current_training)
            saving.save()



