from random import randint


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


if __name__ == '__main__':
    n, m = (int(i) for i in input().split())
    edges = set()
    for i in range(m):
        u, v = (int(i) for i in input().split())
        edges.add(frozenset((u, v)))
    edges = frozenset(edges)

    team_a = {randint(1, n)}
    team_b = set()
    left_players = set(range(1, n + 1)) - team_a
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
        print(-1)
    else:
        for player in left_players:
            if will_be_fully_connected(player, team_a, edges):
                team_a.add(player)
            elif will_be_fully_connected(player, team_b, edges):
                team_b.add(player)
            else:
                print(-1)
                break
        else:
            print(len(team_a))
            print(" ".join(str(player) for player in team_a))
            print(" ".join(str(player) for player in team_b))
