from django.db import models


class DigimonImage(models.Model):
    href = models.URLField(verbose_name="href")
    transparent = models.BooleanField(verbose_name="Transparent")


class DigimonLevel(models.Model):
    level_id = models.IntegerField(verbose_name="id")
    level_name = models.CharField(verbose_name="level", max_length=100)


class DigimonAtribute(models.Model):
    attr_id = models.IntegerField(verbose_name="id")
    attr_name = models.CharField(verbose_name="attribute", max_length=100)


class DigimonField(models.Model):
    field_id = models.IntegerField(verbose_name="id")
    field_name = models.CharField(verbose_name="field", max_length=100)
    image = models.URLField(verbose_name="image")


class DigimonDescription(models.Model):
    origin = models.CharField(verbose_name="origin", max_length=50)
    language = models.CharField(verbose_name="language", max_length=20)
    description = models.TextField(verbose_name="description")


class DigimonSkill(models.Model):
    skill_id = models.IntegerField(verbose_name="id")
    skill_name = models.CharField(verbose_name="skill", max_length=200)
    translation = models.CharField(verbose_name="translation", max_length=200)
    description = models.TextField(verbose_name="description")


class DigimonEvolution(models.Model):
    evo_id = models.IntegerField(verbose_name="id")
    evo_name = models.CharField(verbose_name="digimon", max_length=200)
    evo_condition = models.CharField(verbose_name="condition", max_length=200)
    evo_image = models.URLField(verbose_name="image")
    evo_link = models.URLField(verbose_name="url")


class Digimon(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    antibody = models.BooleanField(verbose_name="xAntibody")
    images = models.ManyToManyField(DigimonImage, related_name="images")
    levels = models.ManyToManyField(DigimonLevel, related_name="levels")
    attributes = models.ManyToManyField(
        DigimonAtribute, related_name="attributes"
    )
    fields = models.ManyToManyField(DigimonField, related_name="fields")
    release_date = models.CharField(verbose_name="releaseDate", max_length=4)
    descriptions = models.ManyToManyField(
        DigimonDescription, related_name="descriptions"
    )
    skills = models.ManyToManyField(DigimonSkill, related_name="skills")
    prior_evos = models.ManyToManyField(
        DigimonEvolution, related_name="priorEvolutions"
    )
    next_evos = models.ManyToManyField(
        DigimonEvolution, related_name="nextEvolutions"
    )
    comments = models.TextField(verbose_name="Comments")
