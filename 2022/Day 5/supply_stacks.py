""" # noqa
Supply Stacks: This is the first and second challenge of the Day 5 of the Advent of Code.
(https://adventofcode.com/2022/day/5#part2)

Objective (Challenge 1):
	Given a starting configuration and a list of moves, determine the top crate on each stack
	with the ordering of the crates during a move following typical stack popping rules.

Objective (Challenge 2):
	Given a starting configuration and a list of moves, determine the top crate on each stack
	with the ordering of the crates during a move being preserved.


Example:
	Given the following list -
	`````````````````````````
		[D]
	[N] [C]
	[Z] [M] [P]
	 1   2   3

	move 1 from 2 to 1
	move 3 from 1 to 3
	move 2 from 2 to 1
	move 1 from 1 to 2
	`````````````````````````

	Move 1 from 2 to 1 means that 1 crate from stack 2 will be moved to stack 1. So afterwards
	the crate positioning will be:

	[D]
	[N] [C]
	[Z] [M] [P]
	 1   2   3

	Move 3 from 1 to 3:

			[Z]
			[N]
	    [C] [D]
	    [M] [P]
	 1   2   3

	Challenge 1 Answer: Report back 'CMZ' as the top crate in each stack when going from 1->3
	is C in stack 1, M in stack 2, and Z in stack 3.


	Move 1 from 2 to 1 means that 1 crate from stack 2 will be moved to stack 1. So afterwards
	the crate positioning will be:

	[D]
	[N] [C]
	[Z] [M] [P]
	 1   2   3

	Move 3 from 1 to 3:

			[D]
			[N]
	    [C] [Z]
	    [M] [P]
	 1   2   3

	Challenge 2 Answer: Report back 'MCD' as the top crate in each stack when going from 1->3
	is M in stack 1, C in stack 2, and D in stack 3.

Author: Ryan Lanciloti
Date of Creation: 12/4/2022
"""
import os
import argparse
import copy

from typing import Tuple, List


def _get_top_crates(stacks: list) -> str:
	"""
	Gets the name of the crate on the top of each stack and concatinates them into a string

	:param list stacks: Stacks to be parsed
	:return str: String representing the top crate in each stack
	"""
	retval = ""
	for stack in stacks:
		retval += stack[-1]
	return retval


def _do_moves(stacks: list, moves: list) -> Tuple[list, list]:
	"""
	Modifies the given stack according to the list of moves.

	A = Challenge 1 output
	B = Challenge 2 output

	:param list stacks: List of stacks to be modified
	:param list moves: List of actions to be taken on the stack
	:return Tuple[list,list]: (A, B)
	"""

	c1_stack = copy.deepcopy(stacks)
	c2_stack = copy.deepcopy(stacks)

	def do_move_ordering_preserved(stacks: list, move: Tuple[int, int, int]):
		"""
		Helper function which does a single move on the stack. Stack ordering preserved during
		the move.

		:param list stacks: List of stacks to be modified
		:param Tuple[int, int, int] move: Tuple representing the move to be made
		"""
		num_crates, move_from, move_to = move
		buffer = [stacks[move_from].pop() for _ in range(num_crates)]
		buffer_size = len(buffer)

		for _ in range(buffer_size):
			stacks[move_to].append(buffer.pop())

	def do_move_ordering_changed(stacks: list, move: Tuple[int, int, int]):
		"""
		Helper function which does a single move on the stack. Stack ordering not preserved
		during the move.

		:param list stacks: List of stacks to be modified
		:param Tuple[int, int, int] move: Tuple representing the move to be made
		"""
		num_crates, move_from, move_to = move
		buffer = [stacks[move_from].pop() for _ in range(num_crates)]
		stacks[move_to].extend(buffer)

	for move in moves:
		do_move_ordering_changed(c1_stack, move)
		do_move_ordering_preserved(c2_stack, move)

	return c1_stack, c2_stack


def _parse_file(file: str) -> Tuple[list, list]:
	"""
	Parses the input file into a the starting configuration and the list of moves
	to be taken. Returns two lists:

	A = List of list objects which represent each stack of crates
	B = List of tuples representing the move (# to move, stack to move from, stack to move to)

	:param str file: File with the starter configuration and moves
	:return Tuple[list, list]: (A, B)
	"""
	def parse_move(line: str) -> Tuple[int, int, int]:
		"""
		Helper function to parse the move statements. The syntax for a move is as follows:
		- `move A from B to C`
		- A = # to move
		- B = stack to move from
		- C = stack to move to

		:param str line: move statement to be parsed
		:return Tuple[int, int, int]: parsed move statement assembled as a tuple
		"""
		parts = line.split()
		return (int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1)

	def parse_stacks(stack_buffer: list) -> List[list]:
		"""
		Helper function to parse through the configuration representing the initial configuration
		of the stacks.

		:param list stack_buffer: List of strings representing the stack configuration
		:return List[list]: List of lists, one for each crate stack
		"""
		crate_name_pos = list()
		stack_buffer = list(reversed(stack_buffer))

		stacks = list()

		for pos, val in enumerate(stack_buffer[0]):
			if val.isnumeric():
				crate_name_pos.append(pos)
				stacks.append(list())

		for line in stack_buffer[1:]:
			for pos, val in enumerate(crate_name_pos):
				if line[val] != " ":
					stacks[pos].append(line[val])

		return stacks

	stacks = list()
	moves = list()

	stacks_buffer = list()

	with open(file, "r") as fptr:
		for line in fptr:
			line = line.strip('\n\r')
			if line.startswith("move"):
				moves.append(parse_move(line))
			else:
				if line:
					stacks_buffer.append(line)

	stacks = parse_stacks(stacks_buffer)

	return stacks, moves


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
	parser = argparse.ArgumentParser("Supply Stacks")

	parser.add_argument(
		"--infile", dest='infile', type=str, required=True,
		help="Path to the input file"
	)

	args = parser.parse_args() if cmd_args is None else parser.parse_args(cmd_args)
	_validate_arguments(args)

	return args


def main(cmd_args: list = None) -> Tuple[str, str]:
	"""
	Main function which will act as an entry point for this script. Returns a tuple
	containing two values: (A, B)

	A = Ordering of the top crates in the stacks with the move ordering changed
	B = Ordering of the top crates in the stacks with the move ordering preserved

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	args = _get_arguments(cmd_args)
	stacks, moves = _parse_file(args.infile)
	c1_stack, c2_stack = _do_moves(stacks, moves)

	return _get_top_crates(c1_stack), _get_top_crates(c2_stack)


if __name__ == '__main__':
	top_crates_ordering_changed, top_crates_ordering_preserved = main()

	print(f"Top crate in each stack (ordering changed): {top_crates_ordering_changed}")
	print(f"Top crate in each stack (ordering preserved): {top_crates_ordering_preserved}")
