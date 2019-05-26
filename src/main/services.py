from .models import Group

# from math import factorial


class Schedule:
    datetime_start = "15-06-2019 19:00"
    match_length = "15"  # Mins

    # def get_matches_by_group(self, group):
    #     """
    #     n: number of teams
    #     fact(n) / (2 * fact(n - 2))

    #     1 -> 0
    #     2 -> 1
    #     3 -> 3
    #     4 -> 6
    #     5 -> 10
    #     6 -> 15
    #     """

    #     number_of_teams = group.teams.count()

    #     return factorial(number_of_teams) / (2 * factorial(number_of_teams - 2))

    @staticmethod
    def get_match_combinations(teams: list):
        """
        Returns the combinations of all teams without repetition.
        Teams playing at home or away should be equal
        """

        result = []
        i = 0
        home = True

        while i < len(teams):
            j = i + 1
            while j < len(teams):
                if home:
                    result.append((teams[i], teams[j]))
                else:
                    result.append((teams[j], teams[i]))
                j += 1
                home = not home
            i += 1

        return result

    def create_matches(self, group: Group):
        """
        Given a group, it should return a list of matches between the teams in that group
        following the FBIB table
        """

        combinations = self.get_match_combinations(teams=group.team_set.all())

        return combinations

    def get_schedule(self):
        for group in Group.objects.all():
            self.create_matches(group)
        # TODO: put matches on fields and time slots
