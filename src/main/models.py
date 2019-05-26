from django.db import models

INF = 0
CAD = 1
ABS = 2

AGES = [
    (INF, "Infantil"),
    (CAD, "Cadet"),
    (ABS, "Absoluta"),
]
SEXES = [
    ('masc', "Masculina"),
    ('fem', "Femenina"),
    ('mix', "Mixta"),
]


class BaseModel(models.Model):
    created = models.DateTimeField(
        "Creado",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        "Actualizado",
        auto_now=True,
    )

    class Meta:
        abstract = True


class Group(BaseModel):
    name = models.CharField(
        "Nom",
        max_length=255,
    )
    category = models.PositiveIntegerField(
        "Categoria",
        choices=AGES,
    )
    modality = models.CharField(
        "Modalitat",
        choices=SEXES,
        max_length=255,
    )

    class Meta:
        verbose_name = "Grup"
        ordering = ['category', 'created']

    def __str__(self):
        return self.name


class Team(BaseModel):
    name = models.CharField(
        "Nom",
        max_length=255,
    )

    category = models.PositiveIntegerField(
        "Categoria",
        choices=AGES,
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
        ordering = ['created']

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
