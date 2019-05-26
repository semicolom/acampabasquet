from django.test import SimpleTestCase

from main.services import Schedule


class ScheduleTestCase(SimpleTestCase):
    def test_get_creuements(self):
        teams = [1, 2, 3]
        result = Schedule.get_match_combinations(teams)
        self.assertEqual(
            result,
            [
                (1, 2), (3, 1),
                (2, 3)
            ]
        )

        teams = [1, 2, 3, 4]
        result = Schedule.get_match_combinations(teams)
        self.assertEqual(
            result,
            [
                (1, 2), (3, 1), (1, 4),
                (3, 2), (2, 4),
                (4, 3)
            ]
        )

        teams = [1, 2, 3, 4, 5]
        result = Schedule.get_match_combinations(teams)
        self.assertEqual(
            result,
            [
                (1, 2), (3, 1), (1, 4), (5, 1),
                (2, 3), (4, 2), (2, 5),
                (4, 3), (3, 5),
                (5, 4),
            ]
        )
