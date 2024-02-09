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


class Career(models.Model):
    name = models.CharField(max_length=64)


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

    )
    careers = models.ManyToManyField(

    )


class Character(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_world = models.ForeignKey(
        "HomeWorld",
        on_delete=models.CASCADE,
        related_name="characters",
    )

    # Characteristics
    characteristics = models.ManyToManyField(
        'Characteristic',
        through=CharacterCharacteristic,
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

