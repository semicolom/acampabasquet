from django.db import models
from django.db.models import Q

INF = 0
CAD = 1
ABS = 2
JUN = 3
SEN = 4
VET = 5

CATEGORIES = [
    (INF, "Infantil"),
    (CAD, "Cadet"),
    (JUN, "Junior"),
    (SEN, "Senior"),
    (VET, "Veterans"),
]

MASC = 'masc'
FEM = 'fem'
MIX = 'mix'

MODALITIES = [
    (MASC, "Masculí"),
    (FEM, "Femení"),
    (MIX, "Mixte"),
]

SINGLE = 'single'
DOUBLE = 'double'

COMPETITION_TYPE_CHOICES = [
    (SINGLE, "Partit unic"),
    (DOUBLE, "Anada i tornada"),
]

GAME_FIELDS_CHOICES = [
    (1, "Pista 1"),
    (2, "Pista 2"),
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
    category = models.PositiveIntegerField(
        "Categoria",
        choices=CATEGORIES,
    )
    modality = models.CharField(
        "Modalitat",
        choices=MODALITIES,
        max_length=255,
    )
    competition_type = models.CharField(
        "Tipus de competicio",
        choices=COMPETITION_TYPE_CHOICES,
        default=SINGLE,
        max_length=20,
    )

    class Meta:
        verbose_name = "Grup"
        ordering = ['category', 'created']
        unique_together = [
            ('category', 'modality'),
        ]

    def __str__(self):
        return f"{self.get_category_display()} {self.get_modality_display()}"

    def double_round(self):
        return self.competition_type == DOUBLE


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


class ForbiddenSlot(models.Model):
    start_time = models.TimeField("Des de les")
    end_time = models.TimeField("Fins les")

    class Meta:
        abstract = True
        verbose_name = "Franja de temps on no poden jugar"
        verbose_name_plural = "Franges de temps on no poden jugar"


class GroupForbiddenSlot(ForbiddenSlot):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )


class TeamForbiddenSlot(ForbiddenSlot):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )


class Match(models.Model):
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
    game_field = models.PositiveSmallIntegerField(
        "Pista",
        choices=GAME_FIELDS_CHOICES,
    )

    my_order = models.PositiveIntegerField(
        "Ordre",
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        verbose_name = "Partit"
        ordering = [
            'my_order',
            'start_time',
        ]

    def __str__(self):
        if self.home_team and self.away_team:
            return f"{self.home_team} vs {self.away_team}"

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
