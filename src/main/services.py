from typing import List

from .models import Team, Group, Match


class Schedule:
    def create_schedule(self):
        matches = []
        group_rounds = {}
        groups = sorted(Group.objects.all(), key=lambda g: g.amount_of_matches, reverse=True)

        for group in groups:
            group_rounds[group.id] = self.get_match_combinations(
                teams=group.team_set.all(),
                double_round=group.double_round,
            )

        round_index = 0
        max_length = 1
        order = 0

        while round_index < max_length:
            for group in groups:
                rounds = group_rounds.get(group.id)
                max_length = max(max_length, len(rounds))

                try:
                    round_matches = rounds[round_index]
                except IndexError:
                    continue

                for home_team, away_team in round_matches:
                    matches.append(
                        Match(
                            home_team=home_team,
                            away_team=away_team,
                            my_order=order,
                        )
                    )
                    order += 1

            round_index += 1

        Match.objects.bulk_create(matches)

    @staticmethod
    def get_match_combinations(
        teams: List[Team],
        double_round: bool = False
    ) -> List[List[tuple]]:
        teams_list = list(teams)
        amount_of_teams = len(teams_list)

        if amount_of_teams < 2:
            raise NotImplementedError

        # Circle method: fix teams_list[0], rotate the rest.
        # For odd amount_of_teams, add a bye (None) so every team gets a rest round.
        if amount_of_teams % 2 == 1:
            teams_list.append(None)

        amount_of_teams_with_bye = len(teams_list)
        fixed_team = teams_list[0]
        rotating_teams = list(teams_list[1:])

        rounds = []
        for round_idx in range(amount_of_teams_with_bye - 1):
            matches = []

            # Fixed team vs last in rotation
            opponent = rotating_teams[-1]
            if fixed_team is not None and opponent is not None:
                if round_idx % 2 == 0:
                    matches.append((fixed_team, opponent))
                else:
                    matches.append((opponent, fixed_team))

            # Remaining slots: pair from outside in
            remaining_teams = rotating_teams[:-1]
            half = len(remaining_teams) // 2
            for i in range(half):
                home_team = remaining_teams[i]
                away_team = remaining_teams[len(remaining_teams) - 1 - i]
                if home_team is not None and away_team is not None:
                    if (round_idx + i + 1) % 2 == 0:
                        matches.append((home_team, away_team))
                    else:
                        matches.append((away_team, home_team))

            rounds.append(matches)

            # Rotate: last element moves to front
            rotating_teams = [rotating_teams[-1]] + rotating_teams[:-1]

        if double_round:
            return_leg = [
                [(away, home) for home, away in round_matches]
                for round_matches in rounds
            ]
            return rounds + return_leg

        return rounds
