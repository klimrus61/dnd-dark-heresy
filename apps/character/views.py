from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Sum, F

from apps.character.froms import CharacterForm, ChooseHomeWorldFrom
from apps.character.models import Character, HomeWorld
from apps.character.utils import choose_random_home_world


class CharacterListView(generic.ListView):
    model = Character
    context_object_name = "characters"
    template_name = "character/list.html"
    queryset = Character.objects.all()


class CharacterDetailView(generic.DetailView):
    model = Character
    context_object_name = "character"
    template_name = "character/detail.html"


class CharacterCreateView(generic.CreateView):
    model = Character
    context_object_name = "character"
    template_name = "character/create.html"
    form_class = CharacterForm


class ChooseHomeWorldView(generic.UpdateView):
    model = Character
    template_name = "character/choose_home_world.html"
    form_class = ChooseHomeWorldFrom


class RandomChooseHomeWorldView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("character-detail", kwargs={"pk": self.kwargs.get("pk")})

    def post(self, request, *args, **kwargs):
        home_worlds = HomeWorld.objects.annotate(roll_weight=F("end_roll")-F("start_roll")).order_by("id")
        chosen_home_world = choose_random_home_world(home_worlds)
        character = Character.objects.get(pk=kwargs.get("pk"))
        character.home_world = chosen_home_world
        character.save()
        return self.get(request, *args, **kwargs)