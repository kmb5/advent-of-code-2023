sample = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

LIMITS = {"red": 12, "green": 13, "blue": 14}


def parse(inp: str):
    games = []

    for game in inp.splitlines():
        parsed_game = []
        _game = game.split(": ")[1]
        draws = _game.split("; ")
        for draw in draws:
            alldraws = {}
            colors = draw.split(", ")
            for color in colors:
                num, col = color.split(" ")
                alldraws[col] = int(num)
            parsed_game.append(alldraws)
        games.append(parsed_game)

    return games


def check_game_possible(game: list[dict]) -> bool:
    for draw in game:
        for color, num in draw.items():
            if num > LIMITS[color]:
                return False

    return True


def check_fewest_cubes(game: list[dict]) -> int:
    """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    maxs = {}

    for draw in game:
        for color, num in draw.items():
            if color not in maxs:
                maxs[color] = num
            elif maxs[color] < num:
                maxs[color] = num

    mult = 1
    for num in maxs.values():
        mult *= num

    return mult


def part1(inp):
    id_sum = 0

    games = parse(inp)
    for i, game in enumerate(games):
        if check_game_possible(game):
            id_sum += i + 1

    return id_sum


def part2(inp):
    mult_sum = 0
    games = parse(inp)
    for game in games:
        mult_sum += check_fewest_cubes(game)

    return mult_sum


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_2_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
