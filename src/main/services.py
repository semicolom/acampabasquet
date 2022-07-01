from typing import List

from .models import Team, Group, Match


class Schedule:
    def create_schedule(self):
        """
        - TODO: Es grup mini ha de jugar tota la lliga al principi
        - Un equip no pot jugar dos partits molt seguits
        - Un equip no pot estar molt de temps sense jugar
        - Un equip hauria de jugar partits separats minim 2h i maxim 3h30min

        - Primer grups amb més partits (així evitam que grups amb pocs partits
            juguin molt prest i hagin d'esperar 8h per ses finals)
        - Grups amb menos partits haurien de tenir més temps de descans
        """

        matches = []
        group_rounds = {}

        for group in Group.objects.all():
            group_rounds[group.id] = self.get_match_combinations(
                teams=group.team_set.all(),
                double_round=group.double_round,
            )

        round_index = 0
        max_length = 1
        order = 0

        while round_index < max_length:
            for group in Group.objects.all():
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

        if len(teams) == 3:
            if double_round:
                # Amb anda i tornada
                return [
                    [
                        (teams[0], teams[1]),  # teams[2] rests
                    ],
                    [
                        (teams[2], teams[0]),  # teams[1] rests
                    ],
                    [
                        (teams[1], teams[2]),  # teams[0] rests
                    ],
                    [
                        (teams[1], teams[0]),  # teams[2] rests
                    ],
                    [
                        (teams[0], teams[2]),  # teams[1] rests
                    ],
                    [
                        (teams[2], teams[1]),  # teams[0] rests
                    ],
                ]

            raise NotImplementedError

        if len(teams) == 4:
            if double_round:
                # Amb anda i tornada
                return [
                    # Anada
                    [
                        (teams[0], teams[1]),
                        (teams[2], teams[3]),
                    ],
                    [
                        (teams[1], teams[2]),
                        (teams[0], teams[3]),
                    ],
                    [
                        (teams[2], teams[0]),
                        (teams[3], teams[1]),
                    ],
                    # Tornada
                    [
                        (teams[1], teams[0]),
                        (teams[3], teams[2]),
                    ],
                    [
                        (teams[2], teams[1]),
                        (teams[3], teams[0]),
                    ],
                    [
                        (teams[0], teams[2]),
                        (teams[1], teams[3]),
                    ],
                ]

            # Sense anda i tornada
            return [
                [
                    (teams[0], teams[1]),
                    (teams[2], teams[3]),
                ],
                [
                    (teams[1], teams[2]),
                    (teams[0], teams[3]),
                ],
                [
                    (teams[2], teams[0]),
                    (teams[3], teams[1]),
                ],
            ]

        if len(teams) == 5:
            return [
                [
                    (teams[0], teams[1]),
                    (teams[2], teams[3]),
                    # teams[4] rests
                ],
                [
                    (teams[4], teams[0]),
                    (teams[1], teams[2]),
                    # teams[3] rests
                ],
                [
                    (teams[4], teams[3]),
                    (teams[0], teams[2]),
                    # teams[1] rests
                ],
                [
                    (teams[1], teams[4]),
                    (teams[3], teams[0]),
                    # teams[2] rests
                ],
                [
                    (teams[2], teams[4]),
                    (teams[3], teams[1]),
                    # teams[0] rests
                ],
            ]

        if len(teams) == 6:
            return [
                [
                    (teams[0], teams[1]),
                    (teams[2], teams[3]),
                    (teams[4], teams[5]),
                ],
                [
                    (teams[1], teams[2]),
                    (teams[5], teams[0]),
                    (teams[4], teams[3]),
                ],
                [
                    (teams[1], teams[4]),
                    (teams[5], teams[3]),
                    (teams[0], teams[2]),
                ],
                [
                    (teams[2], teams[5]),
                    (teams[0], teams[4]),
                    (teams[3], teams[1]),
                ],
                [
                    (teams[3], teams[0]),
                    (teams[1], teams[5]),
                    (teams[2], teams[4]),
                ],
            ]

        if len(teams) == 7:
            return [
                [
                    (teams[0], teams[1]),
                    (teams[2], teams[3]),
                    (teams[4], teams[5]),
                    # teams[6] rests
                ],
                [
                    (teams[6], teams[0]),
                    (teams[1], teams[2]),
                    (teams[3], teams[4]),
                    # teams[5] rests
                ],
                [
                    (teams[5], teams[6]),
                    (teams[0], teams[2]),
                    (teams[1], teams[3]),
                    # teams[4] rests
                ],
                [
                    (teams[5], teams[0]),
                    (teams[2], teams[4]),
                    (teams[6], teams[1]),
                    # teams[3] rests
                ],
                [
                    (teams[3], teams[0]),
                    (teams[4], teams[6]),
                    (teams[1], teams[5]),
                    # teams[2] rests
                ],
                [
                    (teams[0], teams[4]),
                    (teams[2], teams[6]),
                    (teams[3], teams[5]),
                    # teams[1] rests
                ],
                [
                    (teams[4], teams[1]),
                    (teams[5], teams[2]),
                    (teams[6], teams[3]),
                    # teams[0] rests
                ],
            ]

        raise NotImplementedError
