"""
Calorie Counting: This is the first and second challenge of the Day 2 of the Advent of Code.
(https://adventofcode.com/2022/day/2#part2)

Objective (Challenge 1):
	Given a list of rock, paper, scissors moves, figure out your total score given a list of moves
	and the following rules:

	For each round, add the following values to your score if you play them:
	- Rock 		= +1
	- Paper 	= +2
	- Scissors 	= +3

	For each round, add the following values to your score depending on the outcome of the game:
	- Win		= +6
	- Draw		= +3
	- Loss		= +0

	A, X: Rock
	B, Y: Paper
	Z, C: Scissors

Objective (Challenge 2):
	Given a list of rock, paper, scissors moves, figure out your total score given a list of moves
	and the following rules:

	For each round, add the following values to your score if you play them:
	- Rock 		= +1
	- Paper 	= +2
	- Scissors 	= +3

	For each round, add the following values to your score depending on the outcome of the game:
	- Win		= +6
	- Draw		= +3
	- Loss		= +0

	A: Rock
	B: Paper
	Z: Scissors

	X: Lose
	Y: Draw
	Z: Win

Example:
	Given the following list -
	`````````````````````````
	A Y
	B X
	C Z
	`````````````````````````

	Challenge 1 Answer: Report back '15' as rounds 1 + 2 + 3 = 8 + 1 + 6
	Challenge 2 Answer: Report back '12' as rounds 1 + 2 + 3 = 4 + 1 + 7

Author: Ryan Lanciloti
Date of Creation: 12/1/2022
"""
import os
import argparse

from typing import Tuple


_WIN_AMOUNT = 6
_DRAW_AMOUNT = 3
_LOSE_AMOUNT = 0

_SCORE_GUIDE = {
	"X": 1,
	"Y": 2,
	"Z": 3,
}

_WIN_GUIDE = {
	"X": "C",
	"Y": "A",
	"Z": "B"
}

_DRAW_GUIDE = {
	"X": "A",
	"Y": "B",
	"Z": "C"
}

_LOSE_GUIDE = {
	"X": "B",
	"Y": "C",
	"Z": "A"
}

_STRAT_MOVE_GUIDE = {
	"X": {val: key for key, val in _LOSE_GUIDE.items()},
	"Y": {val: key for key, val in _DRAW_GUIDE.items()},
	"Z": {val: key for key, val in _WIN_GUIDE.items()}
}

_STRAT_MOVE_BONUS_GUIDE = {
	"X": _LOSE_AMOUNT,
	"Y": _DRAW_AMOUNT,
	"Z": _WIN_AMOUNT
}


def _get_rps_total(file: str) -> int:
	"""
	Opens a provided file and parses it to get the total score for Rock, Paper, Scissors

	:param str file: File to be opened
	:return int: Total rock, paper, scissors score
	"""
	org_rps_score = 0
	strat_rps_score = 0

	with open(file, "r") as fptr:
		for line in fptr:
			# Challenge 1 Logic
			opponent, user = line.split()
			org_rps_score += _SCORE_GUIDE[user]

			if _WIN_GUIDE[user] == opponent:
				org_rps_score += _WIN_AMOUNT

			if _DRAW_GUIDE[user] == opponent:
				org_rps_score += _DRAW_AMOUNT

			if _LOSE_GUIDE[user] == opponent:
				org_rps_score += _LOSE_AMOUNT

			# Challenge 2 Logic
			strat_rps_score += _STRAT_MOVE_BONUS_GUIDE[user]
			user_move = _STRAT_MOVE_GUIDE[user][opponent]
			strat_rps_score += _SCORE_GUIDE[user_move]

	return org_rps_score, strat_rps_score


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
	parser = argparse.ArgumentParser("Rock, Paper, Scissors")

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

	A = Total rock, paper, scissors score
	B = Total rock, paper, scissors score with the correct strategy

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	args = _get_arguments(cmd_args)
	rps_score_total, strat_rps_score_total = _get_rps_total(args.infile)

	return rps_score_total, strat_rps_score_total


if __name__ == '__main__':
	rps_total_score, strat_rps_total_score = main()

	print(f"Total Score: {rps_total_score}")
	print(f"Total Score With Secret Strategy: {strat_rps_total_score}")
