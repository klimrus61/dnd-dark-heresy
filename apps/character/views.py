from django.shortcuts import render
from django.views import generic

from apps.character.models import Character
from apps.character.froms import CharacterForm, ChooseHomeWorldFrom


class CharacterListView(generic.ListView):
    model = Character
    context_object_name = "characters"
    template_name = 'character/list.html'
    queryset = Character.objects.all()


class CharacterDetailView(generic.DetailView):
    model = Character
    context_object_name = "character"
    template_name = 'character/detail.html'


class CharacterCreateView(generic.CreateView):
    model = Character
    context_object_name = "character"
    template_name = 'character/create.html'
    form_class = CharacterForm


class ChooseHomeWorldView(generic.UpdateView):
    model = Character
    template_name = "character/choose_home_world.html"
    form_class = ChooseHomeWorldFrom
