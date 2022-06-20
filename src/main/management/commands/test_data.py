import random

from django.core.management.base import BaseCommand

from faker import Faker

from main.models import CATEGORIES, MODALITIES, Team, Group, Match


class Command(BaseCommand):
    help = "Creates test fields, groups and teams"

    def clear(self):
        Match.objects.all().delete()
        Group.objects.all().delete()
        Team.objects.all().delete()

    def create_groups(self):
        for category in CATEGORIES:
            for modality in MODALITIES:
                Group.objects.create(
                    category=category[0],
                    modality=modality[0],
                )

    def create_teams(self):
        fake = Faker('dk_DK')

        for group in Group.objects.all():
            for _ in range(1, random.randint(4, 9)):
                Team.objects.create(
                    name=fake.name(),
                    category=group.category,
                    modality=group.modality,
                    group=group,
                )

    def handle(self, *args, **options):
        self.clear()
        self.create_groups()
        self.create_teams()
