from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Character(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_world = models.ForeignKey(

    )

    # Characteristics
    weapon_skill = models.IntegerField()
    ballistic_skill = models.IntegerField()
    strength = models.IntegerField()
    toughness = models.IntegerField()
    agility = models.IntegerField()
    intelligence = models.IntegerField()
    perception = models.IntegerField()
    willpower = models.IntegerField()
    fellowship = models.IntegerField()

    # Career
    career_path = models.ForeignKey(

    )
    # for psyker
    sanctioning_side_effect = models.ForeignKey(

    )

    skills = models.ManyToManyField(
        "Skill",
    )
    talents = models.ManyToManyField(
        "Talent",
    )
    gears = models.ManyToManyField(
        "Gear",
        verbose_name=_("Equipments"),
    )
    rank = models.ForeignKey(
        "Rank",
    )
    traits = models.ManyToManyField(
        "Trait",
    )
    wound = models.IntegerField(verbose_name="HP")
    fate_point = models.IntegerField(verbose_name=_("Fate Points"))
    wealth = models.IntegerField(verbose_name=_("Initial capital"))

    # body
    sex = models.CharField(max_length=1, blank=True)
    age = models.IntegerField(null=True, blank=True)
    hair_color = models.CharField(max_length=32, blank=True)
    eye_color = models.CharField(max_length=32, blank=True)
    skin_color = models.CharField(max_length=32, blank=True)
    quirks = models.ManyToManyField()

    # armour
    armour_head = models.ForeignKey()
    armour_body = models.ForeignKey()
    armour_left_arm = models.ForeignKey()
    armour_right_arm = models.ForeignKey()
    armour_left_leg = models.ForeignKey()
    armour_right_leg = models.ForeignKey()

    # class
    planet_class = models.ForeignKey()

    divination = models.ForeignKey()


class Talent(models.Model):
    name = models.CharField(max_length=255)
    prerequisites = models.TextField(blank=True)
    benefit = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.CharField(max_length=255)
