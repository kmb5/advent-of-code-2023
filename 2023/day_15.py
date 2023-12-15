import re

sample0 = "HASH".split(",")
sample = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""".split(",")


def part1(inp: list[str]):
    sums = 0
    for s in inp:
        sums += get_hash(s)
    return sums


def get_hash(s: str) -> int:
    val = 0
    for code in s.encode("ascii"):
        val += code
        val *= 17
        val = val % 256
    return val


def part2(inp):
    hashes = {}  # so we only have to hash the same value once

    boxes = {k: {} for k in range(256)}
    for s in inp:
        label, op, num = re.search(r"(.*)([=-])(\d?)", s).groups()
        try:
            box = hashes[label]
        except KeyError:
            box = get_hash(label)
            hashes[label] = box

        if op == "-":
            boxes[box].pop(label, None)
        elif op == "=":
            num = int(num)
            if label in boxes[box]:
                boxes[box][label] = num
            else:
                boxes[box].update({label: num})

    total_focusing_power = 0
    for k, v in boxes.items():
        if not v:
            continue

        for i, lens in enumerate(v.values()):
            total_focusing_power += (k + 1) * (i + 1) * lens

    return total_focusing_power


def print_boxes(boxes: dict[str, dict]):
    """just utility for debugging"""
    for k, v in boxes.items():
        if v:
            print(f"Box {k}: {list(v.items())}")


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_15_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read().replace("\n", "").split(",")

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
