from django import forms
from pfreers.models import PfreeEateries

class PfreeEateriesForm(forms.ModelForm):
    class Meta:
        model = PfreeEateries
        #fields = ['eatery_types', 'eatery', 'echolv', 'perf']
        fields = ['eatery_types', 'eatery']
        widgets = {
            'eatery': forms.TextInput(attrs={'class':'form-control'}),
            #'echolv': forms.TextInput(attrs={'class':'form-control'}),
            #'perf': forms.TextInput(attrs={'class':'form-control'}),
        }