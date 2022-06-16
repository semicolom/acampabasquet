from django.db import models
from django.db.models import Q

INF = 0
CAD = 1
ABS = 2
JUN = 3
SEN = 4
VET = 5

MASC = 'masc'
FEM = 'fem'
MIX = 'mix'

CATEGORIES = [
    (INF, "Infantil"),
    (CAD, "Cadet"),
    (JUN, "Junior"),
    (SEN, "Senior"),
    (VET, "Veterans"),
]
MODALITIES = [
    (MASC, "Masculí"),
    (FEM, "Femení"),
    (MIX, "Mixte"),
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
        blank=True,
    )
    category = models.PositiveIntegerField(
        "Categoria",
        choices=CATEGORIES,
    )
    modality = models.CharField(
        "Modalitat",
        choices=MODALITIES,
        max_length=255,
    )
    double_round = models.BooleanField(
        "Doble volta?",
        default=False,
    )

    class Meta:
        verbose_name = "Grup"
        ordering = ['category', 'created']

    def __str__(self):
        if not self.name:
            return f"{self.get_category_display()} {self.get_modality_display()}"
        return self.name


class Team(BaseModel):
    name = models.CharField(
        "Nom",
        max_length=255,
    )

    category = models.PositiveIntegerField(
        "Categoria",
        choices=CATEGORIES,
    )
    modality = models.CharField(
        "Modalitat",
        choices=MODALITIES,
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

    # Contact info
    contact_name = models.CharField(
        "Nom del responsable de l'equip",
        max_length=255,
        blank=True,
    )
    contact_phone = models.CharField(
        "Telèfon del responsable de l'equip",
        max_length=255,
        blank=True,
    )
    contact_email = models.CharField(
        "Correu electrònic de contacte",
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "Equip"
        ordering = [
            '-games_won',
            'games_lost',
            '-points',
            'points_against',
            '-games_played',
            'created',
        ]

    def __str__(self):
        return self.name

    def update_points(self):
        self.points = 0
        self.points_against = 0
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0

        played_matches = Match.objects\
            .filter(Q(home_team=self) | Q(away_team=self))\
            .exclude(Q(home_team_points=0) & Q(away_team_points=0))\
            .distinct()

        self.games_played = len(played_matches)

        for match in played_matches:
            if match.home_team == self:
                self.points += match.home_team_points
                self.points_against += match.away_team_points
                if match.home_team_points > match.away_team_points:
                    self.games_won += 1
                else:
                    self.games_lost += 1
            else:
                self.points += match.away_team_points
                self.points_against += match.home_team_points
                if match.away_team_points > match.home_team_points:
                    self.games_won += 1
                else:
                    self.games_lost += 1

        self.save()


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
        blank=True,
    )

    home_team = models.ForeignKey(
        Team,
        verbose_name="Equip local",
        on_delete=models.PROTECT,
        related_name='games_as_home_team',
        blank=True,
        null=True,
    )
    away_team = models.ForeignKey(
        Team,
        verbose_name="Equip visitant",
        on_delete=models.PROTECT,
        related_name='games_as_away_team',
        blank=True,
        null=True,
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
        if self.home_team and self.away_team:
            name = f"{self.home_team} vs {self.away_team}"
            if self.name:
                name = f"{name} ({self.name})"
            return name

        if self.name:
            return self.name

        return "-"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.home_team and self.away_team:
            self.home_team.update_points()
            self.away_team.update_points()

    @property
    def group(self):
        if self.home_team and self.away_team:
            if self.home_team.group == self.away_team.group:
                return self.home_team.group
        return None
