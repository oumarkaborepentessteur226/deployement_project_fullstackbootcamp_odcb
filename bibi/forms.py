from django.forms import ModelForm
from bibi.models import Document
from django import forms

class formule(ModelForm):
    class Meta:
        model=Document
        fields=['file', 'nom','description']


class DocumentForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={



        }
    ))
    nom = forms.CharField(label='',widget=forms.TextInput(
        attrs={
            'placeholder':'votre nom ici...',


        }
    ))

    description = forms.CharField(label='',widget=forms.Textarea(
        attrs={
            'placeholder':'votre projet ici ...',


        }
    ))