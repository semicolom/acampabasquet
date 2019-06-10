import random

from django.core.management.base import BaseCommand

from main.models import Match


class Command(BaseCommand):
    help = "Adds random results to matches"

    def handle(self, *args, **options):
        for match in Match.objects.all():
            match.home_team_points = random.randint(0, 23)
            match.away_team_points = random.randint(0, 23)
            match.save()
