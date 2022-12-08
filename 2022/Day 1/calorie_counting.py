"""
Calorie Counting: This is the first and second challenge of the Day 1 of the Advent of Code.
(https://adventofcode.com/2022/day/1#part2)

Objective (Challenge 1):
	Given a list of calories that are contained in snacks carried by a group of elves,
	report the total number of calories held by the elf with the most calories.

Objective (Challenge 2):
	Given a list of calories that are contained in snacks carried by a group of elves,
	report the total number of calories carried by the 3 elves with the highest number of calories.

Example:
	Given the following list -
	`````````````````````````
	1000
	2000
	3000

	4000

	5000
	6000

	7000
	8000
	9000

	10000
	`````````````````````````

	Challenge 1 Answer: Report back '24000' as that's what elf 4 has
	Challenge 2 Answer: Report back '45000' as that's the sum of the top three elves calorie count

Author: Ryan Lanciloti
Date of Creation: 12/1/2022
"""
import os
import argparse
from typing import Tuple


def _get_calories_for_each_elf(file: str) -> list:
	"""
	Opens a provided file and parses it to get the calorie count for each elf

	:param str file: File to be opened
	:return list: List with the total calories each elf is holding
	"""
	calorie_list = list()

	with open(file, "r") as fptr:
		for line in fptr:
			if len(calorie_list) == 0 or (line == "\n" and calorie_list[-1] != 0):
				calorie_list.append(0)
			else:
				calorie_list[-1] += int(line.strip("\n\r"))

	return calorie_list


def _validate_arguments(args: argparse.Namespace):
	"""
	This function will validate the arguments provided and raise the proper errors
	"""
	if not os.path.exists(args.infile):
		raise ValueError(f"The provided file does not exist: {args.infile}")


def _get_arguments(cmd_args: list = None) -> argparse.Namespace:
	"""
	Parses through the commandline arguments and returns the namespace with the
	parsed values.

	:return argparse.Namespace: Object containing the commandline arguments
	"""
	parser = argparse.ArgumentParser("Counting Calories of Elves")

	parser.add_argument(
		"--infile", dest='infile', type=str, required=True,
		help="Path to the input file containing the elves calories"
	)

	args = parser.parse_args() if cmd_args is None else parser.parse_args(cmd_args)
	_validate_arguments(args)

	return args


def main(cmd_args: list = None) -> Tuple[int, int]:
	"""
	Main function which will act as an entry point for this script. Returns a tuple
	containing two values: (A, B)

	A = Total number of calories carried by the elf with the most calories
	B = Sum of the top 3 elves holding the most calories

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	args = _get_arguments(cmd_args)
	calorie_list = _get_calories_for_each_elf(args.infile)
	sorted_calorie_list = sorted(calorie_list)

	return sorted_calorie_list[-1], sum(sorted_calorie_list[-3:])


if __name__ == '__main__':
	top_elf, top3_elves = main()

	print(f"Top Elf Calorie Count: {top_elf}")
	print(f"Top 3 Elves Calorie Count: {top3_elves}")
