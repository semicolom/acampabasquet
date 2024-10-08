import codecs
import csv

from django.core.management.base import BaseCommand

from main.constants import CAD, FEM, INF, JUN, MIX, SEN, MASC, MINI
from main.models import Team, Group, Match, SiteConfiguration


class Command(BaseCommand):
    ROW_INDEX_NAME = 2
    ROW_INDEX_CONTACT_NAME = 3
    ROW_INDEX_CONTACT_PHONE = 4
    ROW_INDEX_CONTACT_EMAIL = 1
    ROW_INDEX_CATEGORY = 5
    ROW_INDEX_MODALITY = 6

    def handle(self, *args, **options):
        self.clean_previous_year()
        self.import_teams()
        # self.create_mini_teams()

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
                        contact_name=row[self.ROW_INDEX_CONTACT_NAME],
                        contact_phone=row[self.ROW_INDEX_CONTACT_PHONE],
                        contact_email=row[self.ROW_INDEX_CONTACT_EMAIL],
                        category=self.get_category(row[self.ROW_INDEX_CATEGORY]),
                        modality=self.get_modality(row[self.ROW_INDEX_MODALITY]),
                    )
                )
            Team.objects.bulk_create(teams)
        self.stdout.write(self.style.SUCCESS(f"{Team.objects.count()} teams created!"))

    @staticmethod
    def get_category(csv_category):
        return {
            'INFANTIL (2010/2011)': INF,
            'CADET (2008/2009)': CAD,
            'JUNIOR (2006/2007)': JUN,
            'SENIOR (2005 i posteriors)': SEN,
        }.get(csv_category)

    @staticmethod
    def get_modality(csv_modality):
        return {
            'MASCULÍ': MASC,
            'FEMENÍ': FEM,
            'MIXTE': MIX,
        }.get(csv_modality)

    def create_mini_teams(self):
        """
        7 equipos mini mixtos.
        """

        teams = []
        for index in range(1, 8):
            teams.append(
                Team(
                    name=f"Equip Mini {index}",
                    category=MINI,
                    modality=MIX,
                )
            )
        Team.objects.bulk_create(teams)
