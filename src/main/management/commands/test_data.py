from django.core.management.base import BaseCommand

from main.models import FEM, INF, MIX, SEN, MASC, MINI, DOUBLE, Team, Group, Match


class Command(BaseCommand):
    help = "Creates test fields, groups and teams"

    def handle(self, *args, **options):
        self.clear()
        self.create_groups_and_teams()

    def clear(self):
        Match.objects.all().delete()
        Group.objects.all().delete()
        Team.objects.all().delete()

    def create_groups_and_teams(self):
        # Mini, 7 equips, nomes anada
        group_mini = Group.objects.create(
            name=f"Grup mini",
        )
        for index in range(1, 8):
            Team.objects.create(
                name=f"Equip Mini {index}",
                category=MINI,
                modality=MIX,
                group=group_mini,
            )

        # Inf/Cad masc, 4 equips, anada i tornada
        group_inf_cad_masc = Group.objects.create(
            name=f"Grup Inf/Cad masc",
            competition_type=DOUBLE,
        )
        for index in range(1, 5):
            Team.objects.create(
                name=f"Equip Inf/Cad masc {index}",
                category=INF,
                modality=MASC,
                group=group_inf_cad_masc,
            )

        # Inf/Cad fem, 5 equips, anada
        group_inf_cad_fem = Group.objects.create(
            name=f"Grup Inf/Cad fem",
        )
        for index in range(1, 6):
            Team.objects.create(
                name=f"Equip Inf/Cad fem {index}",
                category=INF,
                modality=FEM,
                group=group_inf_cad_fem,
            )

        # Jun/sen masc, 6 equips, anada
        group_jun_sen_masc = Group.objects.create(
            name=f"Jun/sen masc",
        )
        for index in range(1, 7):
            Team.objects.create(
                name=f"Jun/sen masc {index}",
                category=SEN,
                modality=MASC,
                group=group_jun_sen_masc,
            )

        # Jun/sen fem 1, 4 equips, anada i tornada
        group_jun_sen_fem_1 = Group.objects.create(
            name=f"Jun/sen fem 1",
            competition_type=DOUBLE,
        )
        for index in range(1, 5):  # 4 equips
            Team.objects.create(
                name=f"Jun/sen fem {index}",
                category=SEN,
                modality=FEM,
                group=group_jun_sen_fem_1,
            )

        # Jun/sen fem 2, 4 equips, anada
        group_jun_sen_fem_2 = Group.objects.create(
            name=f"Jun/sen fem 2",
            competition_type=DOUBLE,
        )
        for index in range(6, 10):  # 4 equips
            Team.objects.create(
                name=f"Jun/sen fem {index}",
                category=SEN,
                modality=FEM,
                group=group_jun_sen_fem_2,
            )
