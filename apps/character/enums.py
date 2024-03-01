from django.db import models
from django.utils.translation import gettext as _


class CharacteristicType(models.TextChoices):
    WEAPON_SKILL = "WS", _("Weapon skill")
    BALLISTIC_SKILL = "BS", _("Ballistic skill")
    STRENGTH = "S", _("Strength")
    TOUGHNESS = "T", _("Toughness")
    AGILITY = "Ag", _("Agility")
    INTELLIGENCE = "Int", _("Intelligence")
    PERCEPTION = "Per", _("Perception")
    WILLPOWER = "WP", _("Willpower")
    FELLOWSHIP = "Fel", _("Fellowship")