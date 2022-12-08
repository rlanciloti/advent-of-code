"""
No Space Left On Device: This is the first and second challenge of the Day 7 of the Advent of
Code. (https://adventofcode.com/2022/day/7#part2)

Objective (Challenge 1):
	Given a list of commands and a directory structure with files of various sizes, find the
	total size of all directories that size is (at most) 100000.

Objective (Challenge 2):
	Given a list of commands and a directory structure with files of various sizes, find the
	smallest directory that, when deleted, would allow an update to be applied. Also provided
	is the total size of the files system and the update size

Example:
	Given the following input -
	`````````````````````````
	$ cd /
	$ ls
	dir a
	14848514 b.txt
	8504156 c.dat
	dir d
	$ cd a
	$ ls
	dir e
	29116 f
	2557 g
	62596 h.lst
	$ cd e
	$ ls
	584 i
	$ cd ..
	$ cd ..
	$ cd d
	$ ls
	4060174 j
	8033020 d.log
	5626152 d.ext
	7214296 k
	`````````````````````````

	The resulting directory structure is as follows -
	`````````````````````````
	- / (dir)
	- a (dir)
		- e (dir)
			- i (file, size=584)
		- f (file, size=29116)
		- g (file, size=2557)
		- h.lst (file, size=62596)
	- b.txt (file, size=14848514)
	- c.dat (file, size=8504156)
	- d (dir)
		- j (file, size=4060174)
		- d.log (file, size=8033020)
		- d.ext (file, size=5626152)
		- k (file, size=7214296)
	`````````````````````````

	Challenge 1 Answer: Report back '95437' since directories a and e are the only directories
	less than size 100000 and the sum are their sizes are (94853 + 584).


	The resulting directory sizes are as follows -
	`````````````````````````
	- e: 584
	- a: 94853
	- d: 24933642
	- /: 48381165
	`````````````````````````
	Total size of the file system is 70000000 and needed size is 30000000

	Challenge 2 Answer: Report back '24933642' since 70000000 - 48381165 = 21618835 and
	directory 'd' is the smallest directory that, when deleted, would free up at least
	216188535 units.

Author: Ryan Lanciloti
Date of Creation: 12/6/22
"""
import os
import argparse

from typing import Tuple, List, TextIO

from user_classes import Directory, File

_TOP_LEVEL_DIRECTORY: Directory = Directory("/")
_DIRECTORIES: List[Directory] = [_TOP_LEVEL_DIRECTORY]

_TOTAL_SPACE_AVAILABLE = 70000000
_UPDATE_SIZE = 30000000
_THRESHOLD_SIZE = 100000


def _find_smallest_directory_to_delete() -> int:
	"""
	This function will find the smallest directory which, when deleted, will free up enough
	space to apply the update.

	:return int: Size of the directory to be deleted
	"""
	sorted_directories: List[Directory] = \
		sorted(_DIRECTORIES, key=lambda x: x.size, reverse=True)

	available_space = _TOTAL_SPACE_AVAILABLE - _TOP_LEVEL_DIRECTORY.size
	extra_space_needed = _UPDATE_SIZE - available_space

	last_dir = _TOP_LEVEL_DIRECTORY
	for _dir in sorted_directories:
		if _dir.size >= extra_space_needed:
			last_dir = _dir
		else:
			return last_dir.size


def _get_total_size_of_directories_below_threshold() -> int:
	"""
	This function will loop through all directories and return the total size of all directories
	below a given threshold.

	:return int: Total size of directories
	"""
	total_size = 0
	for _dir in _DIRECTORIES:
		if _dir.size <= _THRESHOLD_SIZE:
			total_size += _dir.size

	return total_size


def _build_directory_structure(args: argparse.Namespace):
	"""
	This function will open the input file and build the correct directory structure as
	described in the input file.

	:param argparse.Namespace args: Namespace containing the commandline arguments
	"""
	def execute_cmd(cwd: Directory, cmd_stream: TextIO):
		"""
		This function will execute the command as provided on the current line in the current
		working directory.

		:param Directory cwd: Current working directory
		:param TextIO cmd_stream: Command to be parsed (or command output)
		"""
		cmd = cmd_stream.readline().split()

		while cmd:
			if cmd[0] == "$" and cmd[1] == "cd":
				if cmd[2] == ".." and cwd != _TOP_LEVEL_DIRECTORY:
					return
				if cmd[2] == "/":
					execute_cmd(_TOP_LEVEL_DIRECTORY, cmd_stream)
				else:
					execute_cmd(cwd.get(cmd[2]), cmd_stream)

			elif cmd[0] == "dir":
				_dir = Directory(cmd[1])
				cwd.add(_dir)
				_DIRECTORIES.append(_dir)

			elif cmd[0].isnumeric():
				cwd.add(File(cmd[1], int(cmd[0])))

			cmd = cmd_stream.readline().split()

	cwd = _TOP_LEVEL_DIRECTORY

	with open(args.infile, "r") as fptr:
		execute_cmd(cwd, fptr)


def _validate_arguments(args: argparse.Namespace):
	"""
	This function will validate the arguments provided and raise the proper errors

	:param argparse.Namespace args: Namespace with the correct arguments
	"""
	if not os.path.exists(args.infile):
		raise ValueError(f"The provided file does not exist: {args.infile}")

	if args.total_size and args.update_size:
		if args.total_size < args.update_size:
			raise ValueError(
				"Space required for the update exceeded the total space available."
			)

	if args.total_size and not args.update_size:
		if args.total_size < _UPDATE_SIZE:
			raise ValueError(
				"Space required for the update exceeded the total space available."
			)

	if not args.total_size and args.update_size:
		if _TOTAL_SPACE_AVAILABLE < args.update_size:
			raise ValueError(
				"Space required for the update exceeded the total space available."
			)


def _get_arguments(cmd_args: list = None) -> argparse.Namespace:
	"""
	Parses through the commandline arguments and returns the namespace with the
	parsed values.

	:return argparse.Namespace: Object containing the commandline arguments
	"""
	# pylint: disable=global-statement
	global _TOTAL_SPACE_AVAILABLE, _UPDATE_SIZE, _THRESHOLD_SIZE

	parser = argparse.ArgumentParser("No Space Left On Device")

	parser.add_argument(
		"--infile", dest='infile', type=str, required=True,
		help="Path to the input file"
	)

	parser.add_argument(
		"--total-size", dest='total_size', type=int, required=False,
		help="Total space available on the device"
	)

	parser.add_argument(
		"--update-size", dest='update_size', type=int, required=False,
		help="Size required for the update"
	)

	parser.add_argument(
		"--size-threshold", dest='size_threshold', type=int, required=False,
		help="Size threshold for directories"
	)

	args = parser.parse_args() if cmd_args is None else parser.parse_args(cmd_args)
	_validate_arguments(args)

	_TOTAL_SPACE_AVAILABLE = _TOTAL_SPACE_AVAILABLE if not args.total_size else args.total_size
	_UPDATE_SIZE = _UPDATE_SIZE if not args.update_size else args.update_size
	_THRESHOLD_SIZE = _THRESHOLD_SIZE if not args.size_threshold else args.size_threshold

	return args


def main(cmd_args: list = None) -> Tuple[int, int]:
	"""
	Main function which will act as an entry point for this script. Returns a tuple
	containing two values: (A, B)

	A = Total size of all directories that are, at most, of size _THRESHOLD_SIZE
	B = Size of the directory which, when deleted, allows for the update to be applied

	Example provided in the file header

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""
	global _TOP_LEVEL_DIRECTORY, _DIRECTORIES  # pylint: disable=global-statement

	# START: Reinitializing globals - Probably should refactor so I'm not using globals
	_TOP_LEVEL_DIRECTORY = Directory("/")
	_DIRECTORIES = [_TOP_LEVEL_DIRECTORY]
	# END: Reinitializing globals - Probably should refactor so I'm not using globals

	args = _get_arguments(cmd_args)
	_build_directory_structure(args)

	return (
		_get_total_size_of_directories_below_threshold(),
		_find_smallest_directory_to_delete()
	)


if __name__ == '__main__':
	retval1, retval2 = main()

	print(
		f"Total size of all directories which are, at most, of size {_THRESHOLD_SIZE}: "
		f"{retval1}"
	)
	print(
		f"Size of the directory which, when deleted, allows for the update to be applied: "
		f"{retval2}"
	)
