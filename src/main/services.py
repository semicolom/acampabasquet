from datetime import timedelta
from typing import List, Tuple

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import Team, Field, Group, Match


class Schedule:
    datetime_start = "2019-06-15 19:30"
    datetime_end = "2019-06-16 19:30"
    available_field_datetime_start = "2019-06-15 23:00"

    match_length = 15  # Mins

    def create_slots(self):
        """
        Returns the list of available slots with the category restrictions.
        Will be used to find the best possible slot
        [
            {
                'time': '19:00',  # Match start time
                'field: 'field_id',  # Match field
                'home_team': 'id_local_team',
                'away_team': 'id_away_team',
                'category': 'inf' / 'cad' / 'abs'
                'free': True / False  # Will help us to identify empty slots
            }
        ]
        """

        slots = []

        fields = list(Field.objects.filter(for_finals=False))
        fields_num = len(fields)
        if fields_num == 0:
            raise Exception("S'han de crear les pistes de joc")
        current_field = 0

        current_time = timezone.make_aware(
            parse_datetime(self.datetime_start),
            timezone.get_default_timezone()
        )
        end_time = timezone.make_aware(
            parse_datetime(self.datetime_end),
            timezone.get_default_timezone()
        )

        available_field_datetime_start = timezone.make_aware(
            parse_datetime(self.available_field_datetime_start),
            timezone.get_default_timezone()
        )

        empty_slot_factor = 60 / self.match_length * fields_num + 1
        free_slot = True
        empty_slots_counter = 1

        while current_time < end_time:
            if current_time >= available_field_datetime_start:
                # Adds free slots every 9 matches (every hour in different fields)
                free_slot = empty_slots_counter % empty_slot_factor != 0

                if not free_slot:
                    Match.objects.create(
                        name="Pista disponible",
                        game_field=fields[current_field],
                        start_time=current_time,
                    )

            slots.append({
                'time': current_time,
                'field': fields[current_field],
                'home_team': None,
                'away_team': None,
                'free': free_slot,
            })

            empty_slots_counter += 1

            current_field = (current_field + 1) % fields_num
            if current_field == 0:
                current_time = current_time + timedelta(minutes=self.match_length)

        return slots

    def get_next_free_slot(self, slots: List, match: Tuple, waiting_time: int):
        home_team = match[0]
        away_team = match[1]

        # Previous match where home_team or away_team played
        previous_matches = Match.objects.filter(
            Q(home_team=home_team) |
            Q(home_team=away_team) |
            Q(away_team=home_team) |
            Q(away_team=away_team)
        )
        if previous_matches.exists():
            previous_match = previous_matches.reverse()[0]

            # Next possible time they can play
            next_possible_time = previous_match.start_time + timedelta(
                minutes=waiting_time
            )
            # previous_field = previous_match.game_field
        else:
            next_possible_time = timezone.make_aware(
                parse_datetime(self.datetime_start),
                timezone.get_default_timezone()
            )
            # previous_field = None

        for slot in slots:
            if (
                slot.get('free') and
                slot.get('time') >= next_possible_time
            ):
                slot['free'] = False
                slot['home_team'] = match[0]
                slot['away_team'] = match[1]
                return slot

    @staticmethod
    def get_match_combinations(teams: List[Team]) -> List[tuple]:
        """
        Returns the combinations of all teams without repetition.
        Teams playing at home or away should be equal
        """

        result = []
        i = 0
        home = True
        small_group = len(teams) < 5

        while i < len(teams):
            j = i + 1
            while j < len(teams):
                if small_group:
                    result.append((teams[i], teams[j]))
                    result.append((teams[j], teams[i]))
                else:
                    if home:
                        result.append((teams[i], teams[j]))
                    else:
                        result.append((teams[j], teams[i]))
                    home = not home
                j += 1
            i += 1

        # random.shuffle(result)

        return result

    @classmethod
    def get_groups_matches(cls) -> dict:
        group_matches = {}

        for group in Group.objects.all():
            teams = group.team_set.all()

            combinations = cls.get_match_combinations(teams)
            # random.shuffle(combinations)

            group_matches[group] = combinations

        return group_matches

    @staticmethod
    def get_waiting_time_by_group(group: Group):
        num_teams = Team.objects.filter(group=group).count()

        if num_teams == 3:
            return 3 * 60  # 3h 00min
        if num_teams == 4:
            return 2 * 60  # 2h 00min
        if num_teams == 5:
            return 3 * 60  # 3h 00min
        if num_teams == 6:
            return 2.5 * 60  # 2h 30min

        return 2 * 60  # 2h 00min

    def create_schedule(self):
        """
        - Un equip no pot jugar dos partits molt seguits
        - Un equip no pot estar molt de temps sense jugar
        - Un equip hauria de jugar partits separats minim 2h i maxim 3h30min
        - Cada hora hi ha d'haver una pista buida
        - Abans de les 23:00 no hi pot haver cap pista buida
        - No hi pot haver grups de menys de 3 equips
        - Grups de 3 i 4 equips fan anada i tornada

        # Equips per grup   # partits per grup  # Partits per equip  Temps de descans entre partits
        3                   6                   4                    3h 00min
        4                   12                  6                    2h 00min
        5                   10                  4                    3h 00min
        6                   15                  5                    2h 30min
        7                   21                  6                    2h 00min
        """

        slots = self.create_slots()
        groups_matches = self.get_groups_matches()

        # Sort groups per amount of matches
        groups_by_amount_of_matches = sorted(
            groups_matches,
            key=lambda k: len(groups_matches[k]),
            reverse=True
        )

        for group in groups_by_amount_of_matches:
            matches = groups_matches[group]
            waiting_time = self.get_waiting_time_by_group(group)
            for match in matches:
                slot = self.get_next_free_slot(slots, match, waiting_time)
                Match.objects.create(
                    home_team=slot.get('home_team'),
                    away_team=slot.get('away_team'),
                    game_field=slot.get('field'),
                    start_time=slot.get('time'),
                )

        return Match.objects.all()
