from django.test import TestCase

from main.models import Match


class MatchTest(TestCase):
    def test_get_start_time(self):
        match = Match.objects.create(my_order=0)
        self.assertEqual(str(match.get_start_time()), "2022-07-01 19:00:00")

        match.my_order = 11
        self.assertEqual(str(match.get_start_time()), "2022-07-01 20:40:00")

        match.my_order = 97
        self.assertEqual(str(match.get_start_time()), "2022-07-02 11:00:00")

    def test_get_field(self):
        match = Match.objects.create(my_order=0)
        self.assertEqual(match.get_field(), 1)

        match.my_order = 11
        self.assertEqual(match.get_field(), 2)

        match.my_order = 97
        self.assertEqual(match.get_field(), 2)
