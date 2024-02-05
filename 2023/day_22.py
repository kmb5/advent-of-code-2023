from __future__ import annotations
from dataclasses import dataclass

sample = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


@dataclass
class Brick:
    x: tuple[int]
    y: tuple[int]
    z: tuple[int]

    @staticmethod
    def parse(s: str) -> Brick:
        starts, ends = s.split("~")
        starts = [int(x) for x in starts.split(",")]
        ends = [int(x) + 1 for x in ends.split(",")]

        return Brick(*zip(starts, ends))

    @property
    def volume(self):
        return (
            (self.x[1] - self.x[0]) * (self.y[1] - self.y[0]) * (self.z[1] - self.z[0])
        )


def part1(inp):
    b = Brick.parse("0,0,1~0,0,10")
    print(b.volume)


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_22_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
