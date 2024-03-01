from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from apps.character.enums import CharacteristicType


User = get_user_model()


class CharacterCharacteristic(models.Model):
    characteristic = models.CharField(
        max_length=4,
        choices=CharacteristicType.choices,
        unique=True
    )
    character = models.ForeignKey(
        "Character",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField()

    def __str__(self):
        return f"{self.characteristic}"

    class Meta:
        db_table = "character_characteristic"


class Divination(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "divination"


class Mutation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "mutation"


class Quirk(models.Model):
    name = models.CharField(max_length=255)
    home_world = models.ForeignKey(
        "HomeWorld",
        on_delete=models.CASCADE,
        related_name="quirks"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "quirk"


class Skill(models.Model):
    class SkillType(models.TextChoices):
        BASIC = "BASIC", _("Basic")
        ADVANCED = "ADVANCED", _("Advanced")

    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=SkillType)
    characteristic = models.CharField(
        max_length=4,
        choices=CharacteristicType.choices,
        unique=True
    )
    descriptor = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "skill"


class Trait(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "trait"


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "career_path"


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "career_rank"


class Gear(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "gear"


class Talent(models.Model):
    name = models.CharField(max_length=255)
    prerequisites = models.TextField(blank=True)
    benefit = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "talent"


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "homeworld"


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "homeworld_class"


class Armour(models.Model):
    class ArmourType(models.TextChoices):
        HEAD = "HEAD", _("Head armour")
        BODY = "BODY", _("Body armour")
        LEFT_ARM = "LEFT_ARM", _("Left arm armour")
        RIGHT_ARM = "RIGHT_ARM", _("Right arm armour")
        LEFT_LEG = "LEFT_LEG", _("Left leg armour")
        RIGHT_LEG = "RIGHT_LEG", _("Right leg armour")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.TextField(choices=ArmourType.choices)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "armour"


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
        blank=True,
    )
    talents = models.ManyToManyField(
        "Talent",
        db_table="character_talent",
        blank=True,
    )
    gears = models.ManyToManyField(
        "Gear",
        db_table="character_gear",
        verbose_name=_("Equipments"),
        blank=True,
    )
    ranks = models.ManyToManyField(
        "CareerRank",
        db_table="character_rank",
        blank=True,
    )
    traits = models.ManyToManyField(
        "Trait",
        db_table="character_trait",
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
        blank=True,
    )

    # armour
    armours = models.ManyToManyField(
        "Armour",
        db_table="character_armour",
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
        blank=True,
        verbose_name=_("Mutations"),
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("character-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = "character"
