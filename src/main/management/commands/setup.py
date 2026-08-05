import codecs
import csv

from django.core.management.base import BaseCommand

from main.constants import CAD, FEM, INF, JUN, MIX, SEN, MASC, MINI, VET
from main.models import Team, Group, Match, SiteConfiguration


class Command(BaseCommand):
    ROW_INDEX_NAME = 0
    ROW_INDEX_CATEGORY = 1
    ROW_INDEX_MODALITY = 2

    def handle(self, *args, **options):
        self.clean_previous_year()
        self.import_teams()

    def clean_previous_year(self):
        Match.objects.all().delete()
        Team.objects.all().delete()
        Group.objects.all().delete()

    def import_teams(self):
        config = SiteConfiguration.get_solo()
        file_path = config.teams_file.path

        with codecs.open(file_path, 'r', 'utf8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip the headers

            teams = []
            for row in reader:
                teams.append(
                    Team(
                        name=row[self.ROW_INDEX_NAME],
                        category=self.get_category(row[self.ROW_INDEX_CATEGORY]),
                        modality=self.get_modality(row[self.ROW_INDEX_MODALITY]),
                    )
                )
            Team.objects.bulk_create(teams)
        self.stdout.write(self.style.SUCCESS(f"{Team.objects.count()} teams created!"))

    @staticmethod
    def get_category(csv_category):
        return {
            'MINI': MINI,
            'INFANTIL': INF,
            'CADET': CAD,
            'JUNIOR': JUN,
            'SENIOR': SEN,
            'VETERANS': VET,
        }[csv_category]

    @staticmethod
    def get_modality(csv_modality):
        return {
            'MASCULÍ': MASC,
            'FEMENÍ': FEM,
            'MIXTE': MIX,
        }[csv_modality]
