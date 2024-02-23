from django import forms

from apps.character_builder.models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name',]
