"""
Rucksack Reorganization: This is the first and second challenge of the Day 3 of the Advent of
Code. (https://adventofcode.com/2022/day/3#part2)

Objective (Challenge 1):
	Given a list of items in various rucksacks, find the common item between each rucksack and sum
	together all of the item's priorities.

	Each rucksack has exactly 2 large containers and will be represented as a string of
	characters. The rucksacks will only ever have ONE
	common character between them

	Item priority is as follows:
		a-z: (1-26)
		A-Z: (27-52)

Objective (Challenge 2):
	Given a list of three rucksacks, find the one item common between each one and sum up the
	priority of these items.

	In a given list, the three rucksacks will appear one after the next. Item priorities
	haven't changed from challenge 1.

Example:
	Given the following list -
	`````````````````````````
	vJrwpWtwJgWrhcsFMMfFFhFp
	jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
	PmmdzqPrVvPwwTWBwg
	wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
	ttgJtRGJQctTZtZT
	CrZsJsPPZsGzwwsLwLmpwMDw
	`````````````````````````

	There are 6 rucksacks (6 lines). Rucksack 1 has two containers:
		Container 1: vJrwpWtwJgWr
		Container 2: hcsFMMfFFhFp

	The common character between the two containers is 'p'.

	Challenge 1 Answer: Report back '157' as the common character priorities sum is:
		16 (p) + 38 (L) + 42 (P) + 22 (v) + 20 (t) + 19 (s)


	There are 6 rucksacks (6 lines), but 2 groups of 3. The groups are as follows:
		Group 1: vJrwpWtwJgWrhcsFMMfFFhFp | jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL | PmmdzqPrVvPwwTWBwg
		Group 2: wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn | ttgJtRGJQctTZtZT | CrZsJsPPZsGzwwsLwLmpwMDw

	Group 1 has the common item 'r' and Group 2 has the common item 'Z'

	Challenge 2 Answer: Report back '70' as the common character priorities sum is: 18 (r) + 52 (Z)

Author: Ryan Lanciloti
Date of Creation: 12/3/2022
"""
import os
import argparse

from typing import Tuple

_BASE_LOWERCASE_PRIORITY = 1
_BASE_UPPERCASE_PRIORITY = 27


def _get_total_priority(file: str) -> Tuple[int, int]:
	"""
	Opens a provided file and parses it to get the rucksack items. Returns a tuple
	containing two values: (A, B)

	A = Total priority of the back rucksack items
	B = Total priority of the badges of authenticity

	:param str file: File to be opened
	:return tuple[int,int]: (A, B)
	"""

	def validate_input(item: str):
		"""
		Validates that the provided input is valid given the constraints of the problem.

		The provided value should be of length 1 and needs to be a letter.

		:param str item: Item to be evaluated.
		:return: N/A
		"""
		if len(item) != 1:
			raise ValueError(
				"Provided rucksack contains two bad values. Please verify inputs."
			)

		if not str(item[0]).isalpha():
			raise ValueError(
				"Provided value is not a value between a-z or A-Z. Please verify inputs."
			)

	priority_sum = 0
	badge_priority_sum = 0
	rucksack_trio = list()

	with open(file, "r") as fptr:
		for rucksack in fptr:
			rucksack = rucksack.strip("\n\r")
			rucksack_trio.append(rucksack)

			# Challenge 1 Logic
			size = len(rucksack)
			if size % 2:
				raise ValueError(
					f"Provided rucksack ({rucksack}) does not contain an even number of entries"
					f" ({size}). Please verify inputs."
				)

			# pylint: disable=invalid-name
			c1 = rucksack[:int(size / 2)]	 # Large container 1
			c2 = rucksack[int(size / 2):]	 # Large container 2

			item = list(set(c1).intersection(c2))
			validate_input(item)

			item = item[0]

			if item.isupper():
				priority_sum += ord(item) - ord('A') + _BASE_UPPERCASE_PRIORITY
			else:
				priority_sum += ord(item) - ord('a') + _BASE_LOWERCASE_PRIORITY

			# Challenge 2 Logic
			if len(rucksack_trio) == 3:
				r1, r2, r3 = rucksack_trio  # pylint: disable=unbalanced-tuple-unpacking

				item = list(set(r1).intersection(set(r2)).intersection(set(r3)))
				validate_input(item)

				item = item[0]

				if item.isupper():
					badge_priority_sum += ord(item) - ord('A') + _BASE_UPPERCASE_PRIORITY
				else:
					badge_priority_sum += ord(item) - ord('a') + _BASE_LOWERCASE_PRIORITY

				rucksack_trio = list()

			# pylint: enable=invalid-name

	return priority_sum, badge_priority_sum


def _validate_arguments(args: argparse.Namespace):
	"""
	This function will validate the arguments provided and raise the proper errors
	"""
	if not os.path.exists(args.infile):
		raise ValueError("The provided file does not exist")


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

	A = Total item priority of the back items in the rucksack
	B = Total badge priority

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	# pylint: disable=redefined-outer-name
	args = _get_arguments(cmd_args)
	total_bad_item_priority, total_badge_item_priority = _get_total_priority(args.infile)

	return total_bad_item_priority, total_badge_item_priority


if __name__ == '__main__':
	total_bad_item_priority, total_badge_item_priority = main()

	print(f"Total priority: {total_bad_item_priority}")
	print(f"Total badge priority score: {total_badge_item_priority}")
