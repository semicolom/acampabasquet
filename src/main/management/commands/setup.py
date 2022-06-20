import csv

from django.core.management.base import BaseCommand

from main.models import CAD, FEM, INF, JUN, MIX, SEN, VET, MASC, Team, Group, Match


class Command(BaseCommand):
    csv_file = "equips.csv"

    def handle(self, *args, **options):
        self.clean_previous_year()
        self.import_teams()

    def clean_previous_year(self):
        Match.objects.all().delete()
        Team.objects.all().delete()
        Group.objects.all().delete()

    def import_teams(self):
        with open(self.csv_file) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip the headers

            teams = []
            for row in reader:
                print(row)
                teams.append(
                    Team(
                        name=row[1],
                        contact_name=row[2],
                        contact_phone=row[3],
                        contact_email=row[4],
                        category=self.get_category(row[5]),
                        modality=self.get_modality(row[6]),
                    )
                )
            Team.objects.bulk_create(teams)

    @staticmethod
    def get_category(csv_category):
        return {
            'INFANTIL (2008/2009)': INF,
            'CADET (2006/2007)': CAD,
            'JUNIOR (2004/2005)': JUN,
            'SENIOR (2003 i posteriors)': SEN,
            'VETERANS (+40)': VET,
        }.get(csv_category)

    @staticmethod
    def get_modality(csv_modality):
        return {
            'MASCULÍ': MASC,
            'FEMENÍ': FEM,
            'MIXTE': MIX,
        }.get(csv_modality)
