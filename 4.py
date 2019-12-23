from random import randint, choice


def find_strangers(team: set, left_players: set, edges: frozenset) -> set:
    strangers = set()
    for player in team:
        for left_player in left_players:
            if {player, left_player} not in edges:
                strangers.add(left_player)
    return strangers


def will_be_fully_connected(new_vertex: int, vertexes: set, edges: frozenset) -> bool:
    for vertex in vertexes:
        if {new_vertex, vertex} not in edges:
            return False
    return True


def merge_commands(team_a1: set, team_b1: set, team_a2: set, team_b2: set, edges: frozenset) -> bool:
    def can_be_merged(team1, team2):
        for player in team2:
            if not will_be_fully_connected(player, team1, edges):
                return False
        return True

    a2_available_commands = set()
    b2_available_commands = set()
    if can_be_merged(team_a1, team_a2):
        a2_available_commands.add(team_a1)
    if can_be_merged(team_b1, team_a2):
        a2_available_commands.add(team_b1)
    if can_be_merged(team_a1, team_b2):
        b2_available_commands.add(team_a1)
    if can_be_merged(team_b1, team_b2):
        b2_available_commands.add(team_b1)

    if not a2_available_commands or not b2_available_commands or \
            (len(a2_available_commands) == 1 and a2_available_commands == b2_available_commands):
        return False

    if len(a2_available_commands) <= len(b2_available_commands):
        chosen_command = choice(tuple(a2_available_commands))
        chosen_command.union(team_a2)
        left_command = team_a1 if team_a1 != chosen_command else team_b1
        left_command.union(team_b2)
    else:
        chosen_command = choice(tuple(b2_available_commands))
        chosen_command.union(team_b2)
        left_command = team_a1 if team_a1 != chosen_command else team_b1
        left_command.union(team_a2)

    return True


def make_commands(people: set, edges: frozenset, good_teams_result=True) -> tuple:
    if not good_teams_result:
        return None, None, False

    team_a = {choice(tuple(people))}
    team_b = set()
    left_players = people - team_a
    good_teams = True
    while good_teams:
        strangers = find_strangers(team_a, left_players, edges)
        new_strangers = strangers - team_b
        for stranger in new_strangers:
            if will_be_fully_connected(stranger, team_b, edges):
                team_b.add(stranger)
                left_players.remove(stranger)
            else:
                good_teams = False
                break
        if not new_strangers:
            break

        strangers = find_strangers(team_b, left_players, edges)
        new_strangers = strangers - team_a
        for stranger in new_strangers:
            if will_be_fully_connected(stranger, team_a, edges):
                team_a.add(stranger)
                left_players.remove(stranger)
            else:
                good_teams = False
                break
        if not new_strangers:
            break

    if not good_teams:
        return None, None, False
    else:
        if left_players:
            team_a2, team_b2, result = make_commands(left_players, edges, good_teams)
            merge_result = merge_commands(team_a, team_b, team_a2, team_b2, edges)
            if not merge_result:
                return None, None, False
        return team_a, team_b, True


if __name__ == '__main__':
    n, m = (int(i) for i in input().split())
    edges = set()
    for i in range(m):
        u, v = (int(i) for i in input().split())
        edges.add(frozenset((u, v)))
    edges = frozenset(edges)

    team_a, team_b, result = make_commands(set(range(1, n + 1)), edges)
    if not result:
        print(-1)
    else:
        print(len(team_a))
        print(" ".join(str(player) for player in team_a))
        print(" ".join(str(player) for player in team_b))
