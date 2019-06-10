from django.test import TestCase

from main.models import INF, Team, Field, Group
from main.services import Schedule


class ScheduleTestCase(TestCase):
    def setUp(self):
        self.group_1 = Group.objects.create(name="Group 1", category=INF)
        self.team_1 = Team.objects.create(name="Team 1", group=self.group_1, category=INF)
        self.team_2 = Team.objects.create(name="Team 2", group=self.group_1, category=INF)
        self.team_3 = Team.objects.create(name="Team 3", group=self.group_1, category=INF)

        self.group_2 = Group.objects.create(name="Group 2", category=INF)
        self.team_4 = Team.objects.create(name="Team 4", group=self.group_2, category=INF)
        self.team_5 = Team.objects.create(name="Team 5", group=self.group_2, category=INF)
        self.team_6 = Team.objects.create(name="Team 6", group=self.group_2, category=INF)
        self.team_7 = Team.objects.create(name="Team 7", group=self.group_2, category=INF)

    def test_get_match_combinations(self):
        with self.subTest("With 3 teams"):
            teams = [self.team_1, self.team_2, self.team_3]

            result = Schedule.get_match_combinations(teams)

            self.assertEqual(
                result,
                [
                    (self.team_1, self.team_2), (self.team_3, self.team_1),
                    (self.team_2, self.team_3)
                ]
            )

        with self.subTest("With 4 teams"):
            teams = [self.team_1, self.team_2, self.team_3, self.team_4]

            result = Schedule.get_match_combinations(teams)

            self.assertEqual(
                result,
                [
                    (self.team_1, self.team_2), (self.team_3, self.team_1),
                    (self.team_1, self.team_4),
                    (self.team_3, self.team_2), (self.team_2, self.team_4),
                    (self.team_4, self.team_3)
                ]
            )

        with self.subTest("With 5 teams"):
            teams = [self.team_1, self.team_2, self.team_3, self.team_4, self.team_5]

            result = Schedule.get_match_combinations(teams)

            self.assertEqual(
                result,
                [
                    (self.team_1, self.team_2), (self.team_3, self.team_1),
                    (self.team_1, self.team_4), (self.team_5, self.team_1),
                    (self.team_2, self.team_3), (self.team_4, self.team_2),
                    (self.team_2, self.team_5),
                    (self.team_4, self.team_3), (self.team_3, self.team_5),
                    (self.team_5, self.team_4),
                ]
            )

    def test_get_schedule(self):
        Field.objects.create(name="Field 1")
        Field.objects.create(name="Field 2")

        matches = Schedule().create_schedule()

        self.assertEqual(len(matches), 9)
