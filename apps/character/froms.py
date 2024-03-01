from django import forms

from apps.character.models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name',]
