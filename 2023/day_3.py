from typing import Union
from pprint import pprint

sample = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

sample2 = """467..114..
...*......
..35...633
617*...#..
..........
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def parse_matrix(mtrx: str) -> list[list[Union[str, int]]]:
    return [[_treat(char) for char in row] for row in mtrx.splitlines()]


def _treat(char: str):
    if char.isdigit():
        return int(char)
    return char


def part1(inp):
    """please close your eyes this is super ugly"""
    sum_all_part_nums = 0
    matrix = parse_matrix(inp)

    i = 0

    while i < len(matrix):
        j = 0
        while j < len(matrix[i]):
            cell = matrix[i][j]

            if isinstance(cell, int):
                end = find_end_of_num(matrix, i, j)
                part_num = int("".join([str(x) for x in matrix[i][j : j + end + 1]]))

                sym = check_cells(matrix, i, j)
                for x in range(j, j + end + 1):
                    sym_ = check_cells(matrix, i, x)
                    if sym is False and sym_ is True:
                        sym = sym_

                if sym:
                    sum_all_part_nums += part_num
                j += end
            j += 1
        i += 1

    return sum_all_part_nums


def part2(inp):
    sum_ratios = 0
    matrix = parse_matrix(inp)

    i = 0
    while i < len(matrix):
        j = 0
        while j < len(matrix[i]):
            cell = matrix[i][j]

            if cell == "*":
                m = count_matching(matrix, i, j)
                if len(m) == 2:
                    sum_ratios += list(m)[0] * list(m)[1]

            j += 1
        i += 1

    return sum_ratios


def find_end_of_num(matrix, i, j):
    j_add = 0
    while True:
        try:
            char = matrix[i][j + j_add]
            if not isinstance(char, int):
                return j_add - 1
            else:
                j_add += 1
        except IndexError:
            return j_add - 1


def find_start_of_num(matrix, i, j):
    j_sub = 0
    while True:
        try:
            char = matrix[i][j + j_sub]
            if not isinstance(char, int):
                return j_sub + 1
            else:
                j_sub -= 1
        except IndexError:
            return j_sub + 1


def count_matching(matrix, i, j):
    matching = set()
    for i_add in (-1, 0, 1):
        for j_add in (-1, 0, 1):
            i_check = i + i_add
            j_check = j + j_add
            if check_cell(matrix, i_check, j_check, int):
                print(f"found int {matrix[i_check][j_check]}")
                start = j_check + find_start_of_num(matrix, i_check, j_check)
                end = j_check + find_end_of_num(matrix, i_check, j_check)
                part_num = int(
                    "".join((str(s) for s in matrix[i_check][start : end + 1]))
                )
                print(part_num)
                matching.add(part_num)

    return matching


def check_cells(matrix, i, j, check_for=str):
    for i_add in (-1, 0, 1):
        for j_add in (-1, 0, 1):
            if check_cell(matrix, i + i_add, j + j_add, check_for):
                return True

    return False


def check_cell(matrix, i, j, check_for=str):
    """return True if its a symbol, false otherwise"""
    try:
        cell = matrix[i][j]
        if isinstance(cell, check_for) and cell != ".":
            return True
    except IndexError:
        return False
    return False


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_3_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
