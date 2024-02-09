from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Characteristic(models.Model):
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

    name = models.CharField(max_length=4, choices=CharacteristicType)


class CharacterCharacteristic(models.Model):
    characteristic = models.ForeignKey(
        "Characteristic",
        on_delete=models.CASCADE,
    )
    character = models.ForeignKey(
        "Character",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField()


class Skill(models.Model):
    class SkillType(models.TextChoices):
        BASIC = "BASIC", _("Basic")
        ADVANCED = "ADVANCED", _("Advanced")

    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=SkillType)
    characteristic = models.ForeignKey(
        "Characteristic",
        on_delete=models.CASCADE,
        related_name="skills",
    )
    descriptor = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Trait(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)


class CareerPath(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    starting_skills = models.ManyToManyField(
        "Skill"
    )
    starting_talents = models.ManyToManyField(
        "Talent"
    )
    starting_gears = models.ManyToManyField(
        "Gear"
    )
    starting_traits = models.ManyToManyField(
        "Trait"
    )


class CareerRank(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    career_path = models.ForeignKey(
        "CareerPath",
        on_delete=models.CASCADE,
        related_name="ranks",
    )
    min_xp = models.IntegerField()
    max_xp = models.IntegerField()
    rank_level = models.IntegerField()




class Talent(models.Model):
    name = models.CharField(max_length=255)
    prerequisites = models.TextField(blank=True)
    benefit = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.CharField(max_length=255)


class HomeWorld(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    life_description = models.TextField(blank=True)
    pc_description = models.TextField(blank=True)
    skills = models.ManyToManyField(
        "Skill",
    )
    traits = models.ManyToManyField(
        "Trait",
    )
    careers = models.ManyToManyField(
        "CareerPath"
    )


class PlanetClass(models.Model):
    """
    A planet-class represents a previous activity of character
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class Character(models.Model):
    name = models.CharField(max_length=64)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_world = models.ForeignKey(
        "HomeWorld",
        on_delete=models.SET_NULL,
        related_name="characters",
        null=True,
        blank=True,
    )

    # Characteristics
    characteristics = models.ManyToManyField(
        'Characteristic',
        through=CharacterCharacteristic,
        null=True,
        blank=True,
    )
    # weapon_skill = models.IntegerField()
    # ballistic_skill = models.IntegerField()
    # strength = models.IntegerField()
    # toughness = models.IntegerField()
    # agility = models.IntegerField()
    # intelligence = models.IntegerField()
    # perception = models.IntegerField()
    # willpower = models.IntegerField()
    # fellowship = models.IntegerField()

    # Career
    career_path = models.ForeignKey(
        "CareerPath",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    skills = models.ManyToManyField(
        "Skill",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    talents = models.ManyToManyField(
        "Talent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gears = models.ManyToManyField(
        "Gear",
        verbose_name=_("Equipments"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ranks = models.ManyToManyField(
        "CareerRank",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    traits = models.ManyToManyField(
        "Trait",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    wound = models.IntegerField(verbose_name="HP", null=True, blank=True)
    fate_point = models.IntegerField(verbose_name=_("Fate Points"), null=True, blank=True)
    wealth = models.IntegerField(verbose_name=_("Initial capital"), null=True, blank=True)

    # body
    sex = models.CharField(max_length=32, blank=True)
    age = models.IntegerField(null=True, blank=True)
    hair_color = models.CharField(max_length=32, blank=True)
    eye_color = models.CharField(max_length=32, blank=True)
    skin_color = models.CharField(max_length=32, blank=True)
    quirks = models.ManyToManyField(
        "Quirks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # armour
    armour_head = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    armour_body = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    armour_left_arm = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    armour_right_arm = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    armour_left_leg = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    armour_right_leg = models.ForeignKey(
        "Gear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # class
    planet_class = models.ForeignKey(
        "PlanetClass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    divination = models.ForeignKey(
        "Divination",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Imperial Divination")
    )

