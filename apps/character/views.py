from django.shortcuts import render
from django.views.generic import CreateView

from apps.character.models import Character
from apps.character.froms import CharacterForm


class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = ''


