from django.test import TestCase

from main.models import FEM, INF, MIX, MASC, DOUBLE, Team, Group, Match
from main.services import Schedule, OldSchedule


class OldScheduleTestCase(TestCase):
    group_1 = None
    group_2 = None

    @classmethod
    def setUpTestData(cls):
        cls.group_1 = Group.objects.create(name="Group 1", category=INF)
        cls.team_1 = Team.objects.create(name="Team 1", group=cls.group_1, category=INF)
        cls.team_2 = Team.objects.create(name="Team 2", group=cls.group_1, category=INF)
        cls.team_3 = Team.objects.create(name="Team 3", group=cls.group_1, category=INF)

        cls.group_2 = Group.objects.create(name="Group 2", category=INF)
        cls.team_4 = Team.objects.create(name="Team 4", group=cls.group_2, category=INF)
        cls.team_5 = Team.objects.create(name="Team 5", group=cls.group_2, category=INF)
        cls.team_6 = Team.objects.create(name="Team 6", group=cls.group_2, category=INF)
        cls.team_7 = Team.objects.create(name="Team 7", group=cls.group_2, category=INF)

    def test_get_match_combinations(self):
        with self.subTest("With 3 teams"):
            teams = [self.team_1, self.team_2, self.team_3]

            result = OldSchedule.get_match_combinations(teams, double_round=True)

            self.assertEqual(
                result,
                [
                    # Ronda 1
                    (self.team_1, self.team_2),
                    (self.team_3, self.team_1),
                    (self.team_2, self.team_3),
                    # Ronda 2
                    (self.team_2, self.team_1),
                    (self.team_1, self.team_3),
                    (self.team_3, self.team_2),
                ]
            )

        with self.subTest("With 4 teams"):
            teams = [self.team_1, self.team_2, self.team_3, self.team_4]

            result = OldSchedule.get_match_combinations(teams, double_round=True)

            self.assertEqual(
                result,
                [
                    # Ronda 1
                    (self.team_1, self.team_2),
                    (self.team_3, self.team_4),
                    (self.team_2, self.team_3),
                    (self.team_4, self.team_1),
                    # Ronda 2
                    (self.team_2, self.team_1),
                    (self.team_4, self.team_3),
                    (self.team_3, self.team_2),
                    (self.team_1, self.team_4),
                ]
            )

        with self.subTest("With 5 teams"):
            teams = [self.team_1, self.team_2, self.team_3, self.team_4, self.team_5]

            result = OldSchedule.get_match_combinations(teams)

            self.assertEqual(
                result,
                [
                    # Ronda 1
                    (self.team_1, self.team_2),
                    (self.team_3, self.team_4),
                    (self.team_5, self.team_1),
                    (self.team_2, self.team_3),
                    (self.team_5, self.team_4),

                    # Ronda 2
                    (self.team_1, self.team_3),
                    (self.team_2, self.team_5),
                    (self.team_4, self.team_1),
                    (self.team_3, self.team_5),
                    (self.team_4, self.team_2),
                ]
            )

    def test_get_schedule(self):
        matches = OldSchedule().create_schedule()

        self.assertEqual(len(matches), 9)


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
        Schedule().create_matches()
        self.assertEqual(
            Match.objects.count(),
            6 + 6  # Group1 3 matches go and return, Group2 6 matches
        )

    def test_create_rounds(self):
        group_3 = Group.objects.create(
            name="Group 3",
            competition_type=DOUBLE,
        )
        n_teams = 3
        for n in range(1, n_teams + 1):
            Team.objects.create(
                name=f"Team 3{n}",
                group=group_3,
                category=INF,
                modality=FEM,
            )
        rounds = list(Schedule.create_rounds(group_3))
        a = 1
