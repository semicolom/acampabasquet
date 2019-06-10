from django.core.management.base import BaseCommand

from main.models import CATEGORIES, MODALITIES, Team, Field, Group, Match


class Command(BaseCommand):
    help = "Regenerates the IndexedProductVariant table"

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
                Group.objects.create(
                    name=f"{category[1]} {modality[1]}",
                    category=category[0],
                    modality=modality[0],
                )

    def create_teams(self):
        category_index = 0
        modality_index = 0

        for category in CATEGORIES:
            for modality in MODALITIES:
                grup = Group.objects.get(
                    category=category[0],
                    modality=modality[0],
                )
                for index in range(1, 6):
                    Team.objects.create(
                        name=f"Equip {index}",
                        category=category[0],
                        modality=modality[0],
                        group=grup,
                    )
                modality_index += 1
            category_index += 1

    def handle(self, *args, **options):
        self.clear()

        self.create_fields()
        self.create_groups()
        self.create_teams()
