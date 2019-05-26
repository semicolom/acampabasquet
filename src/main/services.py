from datetime import timedelta
from typing import List

from django.utils.dateparse import parse_datetime

from .models import Team, Field, Group, Match

# from math import factorial


class Schedule:
    datetime_start = "2019-06-15 19:00"
    match_length = 15  # Mins

    @staticmethod
    def get_match_combinations(teams: List[Team]) -> List[tuple]:
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

    @classmethod
    def get_groups_matches(cls) -> dict:
        group_matches = {}

        for group in Group.objects.all():
            teams = group.team_set.all()
            group_matches[group] = cls.get_match_combinations(teams)

        return group_matches

    def get_schedule(self):
        group_matches = self.get_groups_matches()
        fields = Field.objects.filter(for_finals=False)
        fields_num = len(fields)
        current_field = 0
        match_list = []
        start_time = parse_datetime(self.datetime_start)

        for group, matches in group_matches.items():
            for match in matches:
                home_team = match[0]
                away_team = match[1]
                match = Match(
                    name=f"{home_team} vs. {away_team} ({group})",
                    home_team=home_team,
                    away_team=away_team,
                    game_field=fields[current_field],
                    start_time=start_time,
                )
                match_list.append(match)
                current_field = (current_field + 1) % fields_num
                if current_field == 0:
                    start_time = start_time + timedelta(minutes=self.match_length)

        Match.objects.bulk_create(match_list)

        return match_list
