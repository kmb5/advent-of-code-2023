from __future__ import annotations
from dataclasses import dataclass
import re

sample = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    accepted: bool = False
    rejected: bool = False

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s

    @staticmethod
    def from_str(strdef: str) -> Part:
        parsed = strdef.replace("{", "").replace("}", "").split(",")
        pdict = {}
        for item in parsed:
            splt = item.split("=")
            pdict[splt[0]] = int(splt[1])
        return Part(**pdict)

    def handle_instructions(self, instructions: list[str]):
        if self.accepted is True or self.rejected is True:
            return None
        for instruction in instructions[:-1]:
            instr = re.match(r"([asmx])([<>])(\d+)(:)(\w+)", instruction).groups()
            cat, sign, num, _, res = instr
            if compare(getattr(self, cat), sign, int(num)) is True:
                return self.accept_or_reject(res)
        return self.accept_or_reject(instructions[-1])

    def accept_or_reject(self, res):
        if res == "A":
            self.accepted = True
        elif res == "R":
            self.rejected = True
        else:
            return res


def compare(a, sign, b):
    if sign == "<":
        return a < b
    elif sign == ">":
        return a > b


def parse(inp):
    instructions, parts = inp.split("\n\n")
    instructions = instructions.split("\n")

    parts_list = []
    for p in parts.split("\n"):
        parts_list.append(Part.from_str(p))

    # part_list = [Part(**json.loads) for part in parts]
    parsed_instructions = {}
    for instruction in instructions:
        key, value = re.match(r"(\w+){(.+)}", instruction).groups()
        parsed_instructions[key] = value.split(",")

    return parts_list, parsed_instructions


def part1(inp):
    parts, instructions = parse(inp)
    accepted = []

    for part in parts:
        res = recursive_handle(part, instructions)
        if res.accepted:
            accepted.append(res)

    return sum_all_ratings(accepted)


def sum_all_ratings(parts: list[Part]):
    return sum(part.rating for part in parts)


def recursive_handle(part: Part, instructions: dict[str, str], instr_key="in"):
    current_instruction = instructions[instr_key]
    result = part.handle_instructions(current_instruction)
    if result is None:
        return part
    return recursive_handle(part, instructions, result)


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_19_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp.rstrip())
    print("Part 1: ", part1_sol)

    part2_sol = part2(sample)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
