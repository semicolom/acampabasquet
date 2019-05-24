from django.db import models

AGES = [
    ('inf', "Infantil"),
    ('cad', "Cadet"),
    ('abs', "Absoluta"),
]
SEXES = [
    ('masc', "Masculí"),
    ('fem', "Femení"),
    ('mix', "Mixte"),
]


class Category(models.Model):
    age = models.CharField("Edat", choices=AGES, max_length=255)
    sex = models.CharField("Sexe", choices=SEXES, max_length=255)


class Team(models.Model):
    name = models.CharField("Nom", max_length=255)

    age = models.CharField("Edat", choices=AGES, max_length=255)
    sex = models.CharField("Sexe", choices=SEXES, max_length=255)

    category = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    points = models.PositiveIntegerField("Punts a favor", default=0)
    points_against = models.PositiveIntegerField("Punts en contra", default=0)
    games_played = models.PositiveIntegerField("Partits jugats", default=0)
    games_won = models.PositiveIntegerField("Partits guanyats", default=0)
    games_lost = models.PositiveIntegerField("Partits perduts", default=0)

    class Meta:
        verbose_name = "Equip"


class Field(models.Model):
    name = models.CharField("Nom", max_length=255)
    for_finals = models.BooleanField("Per jugar finals", default=False)


class Match(models.Model):
    name = models.CharField("Nom", max_length=255)

    home_team = models.ForeignKey(
        Team,
        verbose_name="Equip local",
        on_delete=models.PROTECT,
        related_name='games_as_home_team',
    )
    away_team = models.ForeignKey(
        Team,
        verbose_name="Equip visitant",
        on_delete=models.PROTECT,
        related_name='games_as_away_team',
    )

    home_team_points = models.PositiveIntegerField("Punts equip local", default=0)
    away_team_points = models.PositiveIntegerField("Punts equip visitant", default=0)

    start_time = models.DateTimeField()
    game_field = models.ForeignKey(Field, verbose_name="Pista", on_delete=models.PROTECT)
