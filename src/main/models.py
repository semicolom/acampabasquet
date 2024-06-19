import datetime

from django.db import models
from django.db.models import Q

from solo.models import SingletonModel

from main.constants import (
    DOUBLE, SINGLE, CATEGORIES, MODALITIES, MATCH_TYPES, MATCH_TYPE_COMPETITION,
    COMPETITION_TYPE_CHOICES,
)


class SiteConfiguration(SingletonModel):
    available_fields = models.PositiveSmallIntegerField(
        "Pistes disponibles",
        default=2,
    )
    start_datetime = models.DateTimeField(
        "Data",
        default="2024-06-21 19:00",
    )
    match_length = models.PositiveSmallIntegerField(
        "Durada d'un partit",
        default=20,
        help_text="En minuts",
    )
    teams_file = models.FileField(
        "CSV amb els equips",
        upload_to="teams",
        blank=True,
    )

    def __str__(self):
        return "Configuració"

    class Meta:
        verbose_name = "Configuració"


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
        help_text=(
            'Utilitzar per fer grups manuals. Per defecte sera "Categoria Modalitat"'
        )
    )
    competition_type = models.CharField(
        "Tipus de competicio",
        choices=COMPETITION_TYPE_CHOICES,
        default=SINGLE,
        max_length=20,
    )

    class Meta:
        verbose_name = "Grup"
        ordering = ['created']

    def __str__(self):
        return self.name

    @property
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
    competition_points = models.PositiveIntegerField(
        "Punts",
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
            '-competition_points',
            '-games_won',
            '-points',
            'points_against',
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

        played_matches = Match.objects.filter(
            Q(match_type=MATCH_TYPE_COMPETITION)
            & Q(
                Q(home_team=self)
                | Q(away_team=self)
            )
            & Q(
                Q(home_team_points__gt=0)
                | Q(away_team_points__gt=0)
            )
        ).distinct()

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

        self.competition_points = (self.games_won * 2) + self.games_lost

        self.save()


class TeamForbiddenSlot(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    start_time = models.TimeField("Des de les")
    end_time = models.TimeField("Fins les")

    class Meta:
        verbose_name = "Franja de temps on no poden jugar"
        verbose_name_plural = "Franges de temps on no poden jugar"


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
    name = models.CharField(
        "Nom",
        max_length=255,
        blank=True,
        help_text=(
            'Utilitzar per fer partits manuals. Per defecte sera "Equip local vs Equip visitant"'
        )
    )

    home_team_points = models.PositiveIntegerField(
        "Punts equip local",
        default=0,
    )
    away_team_points = models.PositiveIntegerField(
        "Punts equip visitant",
        default=0,
    )

    match_type = models.CharField(
        "Tipus",
        max_length=255,
        choices=MATCH_TYPES,
        default=MATCH_TYPE_COMPETITION,
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
        ]

    def __str__(self):
        if self.home_team and self.away_team:
            teams_string = f"{self.home_team} vs {self.away_team}"
            if self.name:
                return f"{teams_string} ({self.name})"
            return teams_string

        return self.name or "-"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if (
            self.home_team
            and self.away_team
            and (self.home_team_points != 0 or self.away_team_points != 0)
        ):
            self.home_team.update_points()
            self.away_team.update_points()

    @property
    def group(self):
        if self.home_team and self.away_team:
            if self.home_team.group == self.away_team.group:
                return self.home_team.group
        return None

    def get_start_time(self):
        """
        order - start time - amount of +30min I need to add
        1 - 19:00 - 0 - +30m x 0
        2 - 19:00 - 0 - +30m x 0
        3 - 19:30 - 1 - +30m x 1
        4 - 19:30 - 1 - +30m x 1
        5 - 20:00 - 2 - +30m x 2
        6 - 20:00 - 2 - +30m x 2

        # Create a function that given the order retunrs the amount of +30 I need to add.
        # 1 and 2 must be 0
        # 3 and 4 must be 1
        # 5 and 6 must be 2
        # and so on...
        """

        config = SiteConfiguration.get_solo()

        minutes = int(self.my_order / config.available_fields) * config.match_length
        return config.start_datetime + datetime.timedelta(minutes=minutes)

    def get_field(self):
        """
        Even will be field 1
        Odd will be field 2
        """

        config = SiteConfiguration.get_solo()

        return (self.my_order % config.available_fields) + 1

    def get_score(self):
        return f"{self.home_team_points} - {self.away_team_points}"
