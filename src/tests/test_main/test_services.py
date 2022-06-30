from django.test import TestCase

from main.models import FEM, INF, MASC, DOUBLE, Team, Group, Match
from main.services import Schedule


class ScheduleTest(TestCase):
    group_1 = None
    group_2 = None

    @classmethod
    def setUpTestData(cls):
        cls.group_1 = Group.objects.create(
            name="Group 1",
            competition_type=DOUBLE,
        )
        cls.team_11 = Team.objects.create(
            name="Team 11",
            group=cls.group_1,
            category=INF,
            modality=MASC,
        )
        cls.team_12 = Team.objects.create(
            name="Team 12",
            group=cls.group_1,
            category=INF,
            modality=MASC,
        )
        cls.team_13 = Team.objects.create(
            name="Team 13",
            group=cls.group_1,
            category=INF,
            modality=MASC,
        )

        cls.group_2 = Group.objects.create(name="Group 2")
        cls.team_21 = Team.objects.create(
            name="Team 21",
            group=cls.group_2,
            category=INF,
            modality=FEM,
        )
        cls.team_22 = Team.objects.create(
            name="Team 22",
            group=cls.group_2,
            category=INF,
            modality=FEM,
        )
        cls.team_23 = Team.objects.create(
            name="Team 23",
            group=cls.group_2,
            category=INF,
            modality=FEM,
        )
        cls.team_24 = Team.objects.create(
            name="Team 24",
            group=cls.group_2,
            category=INF,
            modality=FEM,
        )

    def test_create_matches(self):
        self.assertEqual(Match.objects.count(), 0)
        Schedule().create_schedule()
        self.assertEqual(
            Match.objects.count(),
            6 + 6  # Group1 3 matches go and return, Group2 6 matches
        )
