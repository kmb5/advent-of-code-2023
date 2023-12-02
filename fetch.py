"""Fetch puzzle input from Advent of Code website
Usage: python fetch.py -d 1 -y 2020
  -> Fetches the puzzle input for 2020 day 1 & creates base file """

import os
import argparse
from pathlib import Path

import requests

HEADERS = {"cookie": f"session={os.environ['AOC_SESSION_COOKIE']}"}
PARENT = Path(__file__).parent
INPUT_DIR = "inputs"
TEMPLATE_PATH = "template.txt"


def fetch_puzzle_input(day, year=2023):
    """Fetches the puzzle input for a given day and year"""

    year_path = PARENT / str(year)
    if not os.path.isdir(year_path):
        os.mkdir(year_path)

    if not os.path.isdir(year_path / INPUT_DIR):
        os.mkdir(year_path / INPUT_DIR)

    input_path = PARENT / year_path / INPUT_DIR / f"day_{day}_input.txt"
    solution_path = PARENT / year_path / f"day_{day}.py"

    if not os.path.isfile(input_path):
        print(f"Fetching puzzle input for {year} day {day}...")
        res = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input",
            headers=HEADERS,
            timeout=5,
        )
        res.raise_for_status()
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(res.text)

        with open(solution_path, "w", encoding="utf-8") as f:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as templatefile:
                template = templatefile.read()
                f.write(template.format(filepath=input_path))
    else:
        print(f"Puzzle input for {year} day {day} already exists.")


def main():
    """Usage:
    python fetch.py -d 1 -y 2020
      -> Fetches the puzzle input for 2020 day 1 & creates base file
    """
    parser = argparse.ArgumentParser()
    days = list(range(1, 26))
    years = list(range(2015, 2024))
    parser.add_argument(
        "-d",
        "--day",
        help="The day of the puzzle to fetch",
        type=int,
        choices=days,
        required=True,
    )
    parser.add_argument(
        "-y",
        "--year",
        help="The year of the puzzle to fetch",
        type=int,
        choices=years,
        default=2022,
    )

    args = parser.parse_args()

    fetch_puzzle_input(args.day, args.year)


if __name__ == "__main__":
    main()
