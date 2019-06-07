from datetime import timedelta
from typing import List

from django.utils.dateparse import parse_datetime

from .models import Team, Field, Group, Match

# from math import factorial


class Schedule:
    datetime_start = "2019-06-15 19:00"
    datetime_end = "2019-06-156 19:00"
    match_length = 15  # Mins

    def create_slots(self):
        """
        Returns the list of available slots with the category restrictions.
        Will be used to find the best possible slot
        [
            {
                'time': '19:00',
                'field: 'field_id',
                'local_team': 'id_local_team',
                'away_team': 'id_away_team',
                'category': 'inf' / 'cad' / 'abs'
                'free': True / False
            }
        ]
        """

        slots = []

        fields = list(Field.objects.filter(for_finals=False))
        fields_num = len(fields)
        if fields_num == 0:
            raise Exception("S'han de crear les pistes de joc")
        current_field = 0

        start_time = parse_datetime(self.datetime_start)
        end_time = parse_datetime(self.datetime_end)
        while start_time < end_time:
            # TODO: Generate empty slots every hour. At 20:00 field 1, at 21:00 field 2...
            slots.append({
                'time': start_time,
                'field': fields[current_field],
                'local_team': None,
                'away_team': None,
                'free': True,  # Redundant, I could use local_team, away_team or category
                'allowed_categories': [],  # TODO
                'category': None,  # TODO
            })

            current_field = (current_field + 1) % fields_num
            if current_field == 0:
                start_time = start_time + timedelta(minutes=self.match_length)

        return slots

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

        fields = list(Field.objects.filter(for_finals=False))
        fields_num = len(fields)
        if fields_num == 0:
            raise Exception("S'han de crear les pistes de joc")
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

"""
Ronda 

Inf 19:00 - 22:00

Cad 22:00 - 00:00

Abs 00:00 - 05:00

Finals Inf

Finals Cad

Finals Abs
"""
