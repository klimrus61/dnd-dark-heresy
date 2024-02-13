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

    class Meta:
        db_table = "character_characteristic"


class Divination(models.Model):
    name = models.CharField(max_length=255)


class Mutation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Quirk(models.Model):
    name = models.CharField(max_length=255)
    home_world = models.ForeignKey(
        "HomeWorld",
        on_delete=models.CASCADE,
        related_name="quirks"
    )


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
        "Skill",
        db_table="career_start_skill",
    )
    starting_talents = models.ManyToManyField(
        "Talent",
        db_table = "career_start_talent",

    )
    starting_gears = models.ManyToManyField(
        "Gear",
        db_table="career_start_gear",
    )
    starting_traits = models.ManyToManyField(
        "Trait",
        db_table = "career_start_trait",
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


class Gear(models.Model):
    name = models.CharField(max_length=255)


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
        db_table = "homeworld_skill"
    )
    traits = models.ManyToManyField(
        "Trait",
        db_table = "homeworld_trait"
    )
    career_paths = models.ManyToManyField(
        "CareerPath",
        db_table="homeworld_career_path"
    )


class HomeWorldClass(models.Model):
    """
    A planet-class represents a previous activity of character
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    home_world = models.ForeignKey(
        "HomeWorld",
        on_delete=models.CASCADE,
        related_name="classes",
    )

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
        through_fields=('characteristic', 'character'),
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
        db_table="character_skill",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    talents = models.ManyToManyField(
        "Talent",
        db_table="character_talent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gears = models.ManyToManyField(
        "Gear",
        db_table="character_gear",
        verbose_name=_("Equipments"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ranks = models.ManyToManyField(
        "CareerRank",
        db_table="character_rank",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    traits = models.ManyToManyField(
        "Trait",
        db_table="character_trait",
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
        "Quirk",
        db_table="character_quirk",
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
    home_world_class = models.ForeignKey(
        "HomeWorldClass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Home World Class")
    )

    divination = models.ForeignKey(
        "Divination",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Imperial Divination")
    )

    mutations = models.ManyToManyField(
        "Mutation",
        db_table="character_mutation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Mutations"),
    )