from django.core.management.base import BaseCommand
from math import factorial


class Command(BaseCommand):
    """
    Creates the match schedule. It needs:
    - Datetime start
    - List of teams
    - List of categories
    - List of fields
    """

    help = "Creates the match schedule"

    datetime_start = "15-06-2019 19:00"
    match_lenght = "15"  # Mins

    def get_matches_by_group(self, group):
        """
        n: number of teams
        fact(n) / (2 * fact(n - 2))

        1 -> 0
        2 -> 1
        3 -> 3
        4 -> 6
        5 -> 10
        6 -> 15
        """

        number_of_teams = group.teams.count()

        return factorial(number_of_teams) / (2 * factorial(number_of_teams - 2))

    def get_schedule(self):
        """
        Output:
        list of: Time - Match name - Field name
        """

        pass

    def handle(self, *args, **kwargs):
        schedule = self.get_schedule()
        return schedule

        # self.stdout.write("It's now %s" % time)
