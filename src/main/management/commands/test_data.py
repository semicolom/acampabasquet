from django.core.management.base import BaseCommand

from faker import Faker

from main.models import CATEGORIES, MODALITIES, Team, Field, Group, Match
import random


class Command(BaseCommand):
    help = "Creates test fields, groups and teams"

    def clear(self):
        Match.objects.all().delete()
        Group.objects.all().delete()
        Team.objects.all().delete()
        Field.objects.all().delete()

    @staticmethod
    def create_fields():
        Field.objects.create(
            name="Pista 1",
        )
        Field.objects.create(
            name="Pista 2",
        )
        Field.objects.create(
            name="Pista central",
            for_finals=True,

        )

    def create_groups(self):
        for category in CATEGORIES:
            for modality in MODALITIES:
                for index in range(1, 3):
                    Group.objects.create(
                        name=f"{category[1]} {modality[1]} grup {index}",
                        category=category[0],
                        modality=modality[0],
                    )

    def create_teams(self):
        category_index = 0
        modality_index = 0

        fake = Faker('dk_DK')

        for category in CATEGORIES:
            for modality in MODALITIES:
                grups = Group.objects.filter(
                    category=category[0],
                    modality=modality[0],
                )
                for group in grups:
                    for index in range(1, random.randint(4, 7)):
                        Team.objects.create(
                            name=fake.name().split()[1],
                            category=category[0],
                            modality=modality[0],
                            group=group,
                        )
                modality_index += 1
            category_index += 1

    def handle(self, *args, **options):
        self.clear()

        self.create_fields()
        self.create_groups()
        self.create_teams()
