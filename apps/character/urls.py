from django.urls import path

from apps.character import views

urlpatterns = [
    path("", views.CharacterListView.as_view(), name="character-list"),
    path(
        "characters/<int:pk>/",
        views.CharacterDetailView.as_view(),
        name="character-detail",
    ),
    path(
        "characters/create/",
        views.CharacterCreateView.as_view(),
        name="character-create",
    ),
    path(
        "characters/<int:pk>/home-world/",
        views.ChooseHomeWorldView.as_view(),
        name="character-home-world",
    ),
]
