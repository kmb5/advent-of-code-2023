from __future__ import annotations
from pprint import pprint

sample = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


class Beam:
    def __init__(self, x: int = 0, y: int = 0, direction: str = "r"):
        self.x = x
        self.y = y
        self.direction = direction

    def __str__(self):
        if self.direction == "u":
            return "^"
        if self.direction == "d":
            return "v"
        if self.direction == "r":
            return ">"
        if self.direction == "l":
            return "<"

    def __repr__(self):
        return f"{str(self)}({self.x}{self.y})"

    def handle_move(self, move: str) -> list[Beam]:
        if move == "/":
            if self.direction == "r":
                return [Beam(self.x, self.y, "u")]
            if self.direction == "l":
                return [Beam(self.x, self.y, "d")]
            if self.direction == "u":
                return [Beam(self.x, self.y, "r")]
            if self.direction == "d":
                return [Beam(self.x, self.y, "l")]

        elif move == "\\":  # \
            if self.direction == "l":
                return [Beam(self.x, self.y, "u")]
            if self.direction == "r":
                return [Beam(self.x, self.y, "d")]
            if self.direction == "u":
                return [Beam(self.x, self.y, "l")]
            if self.direction == "d":
                return [Beam(self.x, self.y, "r")]

        elif move == "-":
            if self.direction in ("u", "d"):
                return [Beam(self.x, self.y, "l"), Beam(self.x, self.y, "r")]

        elif move == "|":
            if self.direction in ("l", "r"):
                return [Beam(self.x, self.y, "u"), Beam(self.x, self.y, "d")]

        return [Beam(**self.__dict__)]

    def move(self) -> None:
        if self.direction == "u":
            self.y -= 1
        elif self.direction == "d":
            self.y += 1
        elif self.direction == "l":
            self.x -= 1
        elif self.direction == "r":
            self.x += 1
        else:
            raise ValueError("Unknown direction")


def print_frame(grid: list[str], path: dict) -> None:
    to_print = [[i for i in row] for row in grid]
    for coord, beam in path.items():
        x, y = coord
        pos = to_print[y][x]
        if pos == ".":
            to_print[y][x] = beam
        elif pos in ("^", "v", ">", "<"):
            to_print[y][x] = 2
        elif isinstance(pos, int):
            to_print[y][x] += 1

    for row in to_print:
        print("".join(str(i) for i in row))

    print()


def cnt_dist_beams(blist):
    d = {}
    for b in blist.values():
        d[(b.x, b.y)] = None
    return len(d)


def num_energized_beams(data):
    grid, start_beam = data
    curr_beams = {(start_beam.x, start_beam.y, start_beam.direction): start_beam}

    n_energized_last_x_frames = []
    max_n_energized = 10

    frame = 0
    while True:
        # print(f"Frame {frame}")
        new_currs = []
        for curr_beam in curr_beams.values():
            next_move = grid[curr_beam.y][curr_beam.x]
            next_beams = curr_beam.handle_move(next_move)

            for nb in next_beams:
                nb.move()
                if nb.y >= 0 and nb.y < len(grid) and nb.x >= 0 and nb.x < len(grid[0]):
                    new_currs.append(nb)

        for b in new_currs:
            if curr_beams.get((b.x, b.y, b.direction)) is None:
                curr_beams[(b.x, b.y, b.direction)] = b

        # print(n_energized_last_x_frames)
        if len(n_energized_last_x_frames) > max_n_energized:
            if len(set(n_energized_last_x_frames)) == 1:
                return n_energized_last_x_frames[0]
            n_energized_last_x_frames.pop(0)
        n_energized_last_x_frames.append(cnt_dist_beams(curr_beams))

        frame += 1


def part1(inp: str):
    grid = inp.splitlines()
    return num_energized_beams((grid, Beam()))


def part2(inp):
    "super mega ugly brute force code please close your eyes it is horrible"
    from multiprocessing import Pool

    grid = inp.splitlines()
    top = [Beam(x, 0, "d") for x in range(len(grid))]
    bottom = [Beam(x, len(grid) - 1, "u") for x in range(len(grid))]
    left = [Beam(0, x, "r") for x in range(len(grid))]
    right = [Beam(len(grid) - 1, x, "l") for x in range(len(grid))]

    maxtiles = 0

    s = [(grid, i) for i in top]
    with Pool() as p:
        res = p.map(num_energized_beams, s)
        maxtiles = max(maxtiles, max(res))
    print(maxtiles)

    s = [(grid, i) for i in bottom]
    with Pool() as p:
        res = p.map(num_energized_beams, s)
        maxtiles = max(maxtiles, max(res))
    print(maxtiles)

    s = [(grid, i) for i in left]
    with Pool() as p:
        res = p.map(num_energized_beams, s)
        maxtiles = max(maxtiles, max(res))
    print(maxtiles)

    s = [(grid, i) for i in right]
    with Pool() as p:
        res = p.map(num_energized_beams, s)
        maxtiles = max(maxtiles, max(res))
    print(maxtiles)

    return maxtiles


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_16_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
