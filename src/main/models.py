from django.db import models

AGES = [
    ('inf', "Infantil"),
    ('cad', "Cadet"),
    ('abs', "Absoluta"),
]
SEXES = [
    ('masc', "Masculina"),
    ('fem', "Femenina"),
    ('mix', "Mixta"),
]


class Group(models.Model):
    name = models.CharField(
        "Nom",
        max_length=255,
    )
    category = models.CharField(
        "Categoria",
        choices=AGES,
        max_length=255,
    )
    modality = models.CharField(
        "Modalitat",
        choices=SEXES,
        max_length=255,
    )

    class Meta:
        verbose_name = "Grup"

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(
        "Nom",
        max_length=255,
    )

    category = models.CharField(
        "Categoria",
        choices=AGES,
        max_length=255,
    )
    modality = models.CharField(
        "Modalitat",
        choices=SEXES,
        max_length=255,
    )

    group = models.ForeignKey(
        Group,
        verbose_name="Grup",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    points = models.PositiveIntegerField(
        "Punts a favor",
        default=0,
    )
    points_against = models.PositiveIntegerField(
        "Punts en contra",
        default=0,
    )
    games_played = models.PositiveIntegerField(
        "Partits jugats",
        default=0,
    )
    games_won = models.PositiveIntegerField(
        "Partits guanyats",
        default=0,
    )
    games_lost = models.PositiveIntegerField(
        "Partits perduts",
        default=0,
    )

    class Meta:
        verbose_name = "Equip"

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(
        "Nom",
        max_length=255,
    )
    for_finals = models.BooleanField(
        "Per jugar finals",
        default=False,
    )

    class Meta:
        verbose_name = "Pista"
        verbose_name_plural = "Pistes"

    def __str__(self):
        return self.name


class Match(models.Model):
    name = models.CharField(
        "Nom",
        max_length=255,
    )

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

    home_team_points = models.PositiveIntegerField(
        "Punts equip local",
        default=0,
    )
    away_team_points = models.PositiveIntegerField(
        "Punts equip visitant",
        default=0,
    )

    start_time = models.DateTimeField("Hora de joc")
    game_field = models.ForeignKey(
        Field,
        verbose_name="Pista",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Partit"
        ordering = [
            'start_time',
            'game_field',
        ]

    def __str__(self):
        return self.name
