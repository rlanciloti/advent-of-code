"""
{PROPER_NAME}: This is the first and second challenge of the Day {DAY} of the Advent of Code.
(https://adventofcode.com/2022/day/{DAY}#part2)

Objective (Challenge 1):

Objective (Challenge 2):


Example:
	Given the following input -
	`````````````````````````

	`````````````````````````

	Challenge 1 Answer:

	Challenge 2 Answer:

Author: Ryan Lanciloti
Date of Creation: {DATE}
"""
import os
import argparse

from typing import Tuple


def _validate_arguments(args: argparse.Namespace):
	"""
	This function will validate the arguments provided and raise the proper errors

	:param argparse.Namespace args: Namespace with the correct arguments
	"""
	if not os.path.exists(args.infile):
		raise ValueError(f"The provided file does not exist: {args.infile}")


def _get_arguments(cmd_args: list = None) -> argparse.Namespace:
	"""
	Parses through the commandline arguments and returns the namespace with the
	parsed values.

	:return argparse.Namespace: Object containing the commandline arguments
	"""
	parser = argparse.ArgumentParser("{PROPER_NAME}")

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

	A = 0
	B = 0

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	# pylint: disable=redefined-outer-name
	args = _get_arguments(cmd_args)

	return 0, 0


if __name__ == '__main__':
	retval1, retval2 = main()

	print(f"MSG1: {retval1}")
	print(f"MSG2: {retval2}")
