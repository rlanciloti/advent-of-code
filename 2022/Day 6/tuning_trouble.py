"""
Supply Stacks: This is the first and second challenge of the Day 6 of the Advent of Code.
(https://adventofcode.com/2022/day/6#part2)

Objective (Challenge 1):
	Given a string of characters, determine at what point the first sequence of 4 unique
	characters appear.

Objective (Challenge 2):
	Given a string of characters, determine at what point the first sequence of 14 unique
	characters appear.


Example:
	Given the following input -
	`````````````````````````
	bvwbjplbgvbhsrlpgdmjqwftvncz
	`````````````````````````

	Challenge 1 Answer: Report back '5' as 'vwbj' is the first instance of 4 unique
	characters appearing.

	Given the following input -
	`````````````````````````
	mjqjpqmgbljsphdztnvjfqwrcgsmlb
	`````````````````````````

	Challenge 2 Answer: Report back '19' as 'qmgbljsphdztnv' is the first instance of 14 unique
	characters appearing.

Author: Ryan Lanciloti
Date of Creation: 12/5/2022
"""
import os
import argparse

from typing import Tuple


def _find_unique_string_index(file: str, num_unique_characters) -> int:
	"""
	Parses the input file and determines the number of characters that must be parsed before
	the num_unique_characters consecutive, unique characters are found.

	:param str file: File with the starter configuration and moves
	:param int num_unique_characters: Number of consecutive unique characters that need to
	appear
	:return int: Index of last consecutive character
	"""
	input_str = ""

	with open(file, "r") as fptr:
		input_str = fptr.readline()

	for index in range(len(input_str) - num_unique_characters):
		found = True
		buffer = list(input_str[index:index + num_unique_characters])
		buffer.sort()

		for buffer_index in range(len(buffer) - 1):
			if buffer[buffer_index] == buffer[buffer_index + 1]:
				found = False

		if found:
			return index + num_unique_characters

	return -1


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
	parser = argparse.ArgumentParser("Tuning Trouble")

	parser.add_argument(
		"--infile", dest='infile', type=str, required=True,
		help="Path to the input file"
	)

	args = parser.parse_args() if cmd_args is None else parser.parse_args(cmd_args)
	_validate_arguments(args)

	return args


def main(cmd_args: list = None) -> Tuple[int, int]:
	"""
	Main function which will act as an entry point for this script. Returns a tuple
	containing two values: (A, B)

	A = Number of characters that need to be processed before the first unique string
	is found.
	B = 0

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	# pylint: disable=redefined-outer-name
	args = _get_arguments(cmd_args)
	tx_start = _find_unique_string_index(args.infile, 4)
	tx_msg = _find_unique_string_index(args.infile, 14)

	return tx_start, tx_msg


if __name__ == '__main__':
	tx_start, tx_msg = main()

	print(f"Transmit start final character index: {tx_start}")
	print(f"Transmit message final character index: {tx_msg}")
