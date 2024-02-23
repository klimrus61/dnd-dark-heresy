from django.shortcuts import render
from django.views.generic import CreateView

from apps.character_builder.models import Character
from apps.character_builder.froms import CharacterForm


class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = ''


