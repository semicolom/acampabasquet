import random

from django.core.management.base import BaseCommand

from main.models import Match, Team


class Command(BaseCommand):
    help = "Sets all team points to 0"

    def handle(self, *args, **options):
        for team in Team.objects.all():
            team.points = 0
            team.points_against = 0
            team.games_played = 0
            team.games_won = 0
            team.games_lost = 0
            team.competition_points = 0
            team.save()
