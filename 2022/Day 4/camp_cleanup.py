"""
Camp Cleanup: This is the first and second challenge of the Day 4 of the Advent of Code.
(https://adventofcode.com/2022/day/4#part2)

Objective (Challenge 1):
	Given a list of two number ranges, determine how many number ranges fully contain the
	other.

Objective (Challenge 2):
	Given a list of two number ranges, determine how many number ranges overlap one another
	at all.

Example:
	Given the following list -
	`````````````````````````
	2-4,6-8
	2-3,4-5
	5-7,7-9
	2-8,3-7
	6-6,4-6
	2-6,4-8
	`````````````````````````

	Each provided range is inclusive, i.e. 2-4 means (2, 3, 4)

	Thus the above ranges can be represented as follows:
	.234.....  2-4
	.....678.  6-8

	.23......  2-3
	...45....  4-5

	....567..  5-7
	......789  7-9

	.2345678.  2-8
	..34567..  3-7

	.....6...  6-6
	...456...  4-6

	.23456...  2-6
	...45678.  4-8

	Challenge 1 Answer: Report back '2' as pair 4 and pair 5 have two ranges where one fully
	encompases the other.

	Challenge 2 Answer: Report back '4' as pairs 3, 4, 5, and 6 all have ranges which overlap
	the other to some degree.

Author: Ryan Lanciloti
Date of Creation: 12/3/2022
"""
import os
import argparse

from typing import Tuple


def _get_total_redundant_ranges(file: str) -> Tuple[int, int]:
	"""
	Opens a provided file and parses it to get the different search ranges that fully enclose
	one another. Returns a tuple containing two values: (A, B)

	A = Total number of ranges which enclose the other
	B = Total number of ranges that overlap the other at all

	:param str file: File to be opened
	:return tuple[int,int]: (A, B)
	"""
	# pylint: disable=redefined-outer-name
	total_redundant_ranges = 0
	total_overlapping_ranges = 0

	with open(file, "r") as fptr:
		for ranges in fptr:
			range1, range2 = ranges.strip("\n\r").split(",")
			range1 = [int(val) for val in range1.split("-")]
			range2 = [int(val) for val in range2.split("-")]

			if (
				(range1[0] <= range2[0] and range1[1] >= range2[1]) or 	# Case: Range 2 is inside of range 1
				(range1[0] >= range2[0] and range1[1] <= range2[1])   	# Case: Range 1 is inside of range 2
			):
				total_redundant_ranges += 1
				total_overlapping_ranges += 1
			else:
				if (
					# pylint: disable=line-too-long,too-many-boolean-expressions
					(range1[0] <= range2[0] and range1[1] >= range2[0]) or  # Case: Range 1 encompasses range 2 lower bound  # noqa: E501
					(range1[0] <= range2[1] and range1[1] >= range2[1]) or  # Case: Range 1 encompasses range 2 upper bound  # noqa: E501
					(range2[0] <= range1[0] and range2[1] >= range1[0]) or  # Case: Range 2 encompasses range 1 lower bound  # noqa: E501
					(range2[0] <= range1[1] and range2[1] >= range1[1])		# Case: Range 2 encompasses range 1 upper bound  # noqa: E501
					# pylint: enable=line-too-long,too-many-boolean-expressions
				):
					total_overlapping_ranges += 1

	return total_redundant_ranges, total_overlapping_ranges


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

	A = Number of ranges which fully enclose eachother
	B = Number of ranges which overlap at all

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	# pylint: disable=redefined-outer-name
	args = _get_arguments(cmd_args)
	total_range_overlaps, total_overlapping_ranges = _get_total_redundant_ranges(args.infile)

	return total_range_overlaps, total_overlapping_ranges


if __name__ == '__main__':
	total_range_overlaps, total_overlapping_ranges = main()

	print(f"Total fully contained overlapping search ranges: {total_range_overlaps}")
	print(f"Total overlapping search ranges: {total_overlapping_ranges}")
