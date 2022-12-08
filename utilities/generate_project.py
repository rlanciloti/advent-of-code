"""
This script will be used to generate a project based on the template project

Author: Ryan Lanciloti
Date of Creation: 12/6/22
"""
# pylint: disable=bad-indentation,unspecified-encoding

import os
from datetime import datetime
import argparse

_REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _string_replacement(line: str, args: argparse.Namespace) -> str:
	"""
	This function will take a line and replace certain parameters in it with values specified
	in the commandline arguments

	:param str: Line to be modified
	:param argparse.Namespace args: Arguments used to modify the given line
	:return str: The modified line
	"""
	date = datetime.now()
	date_str = f"{date.month}/{date.day}/{str(date.year)[-2:]}"

	try:
		return line.format(
			DATE = date_str,
			DAY = args.day,
			PROPER_NAME = args.proper_name,
			MODULE_NAME = args.module_name
		)
	except KeyError:  # line contains {} that shouldn't be replaced TODO: Add better fix
		return line


def _generate_project(args: argparse.Namespace):
	"""
	This function will generate the new project in the correct location

	:param argparse.Namespace args: Namespace with the correct arguments
	"""
	project_root = os.path.join(_REPO_ROOT, str(args.year), f"Day {args.day}")
	template_directory = os.path.join(_REPO_ROOT, "utilities", "template_project")

	os.makedirs(project_root)  									# Create Project Directory
	os.makedirs(os.path.join(project_root, "test_inputs"))  	# Create Test Inputs Directory
	os.makedirs(os.path.join(project_root, "test_outputs"))  	# Create Test Outputs Directory

	main_py_file = os.path.join(project_root, f"{args.module_name}.py")
	test_py_file = os.path.join(project_root, f"test_{args.module_name}.py")

	main_py_file_template = os.path.join(template_directory, "module.py")
	test_py_file_template = os.path.join(template_directory, "test_module.py")

	with open(main_py_file, "w") as py_file:
		with open(main_py_file_template, "r") as template_file:
			for line in template_file:
				if line == '# type: ignore':
					continue
				py_file.write(_string_replacement(line, args))

	with open(test_py_file, "w") as py_file:
		with open(test_py_file_template, "r") as template_file:
			for line in template_file:
				if line == '# type: ignore':
					continue
				py_file.write(_string_replacement(line, args))


def _validate_arguments(args: argparse.Namespace):
	"""
	This function will validate the arguments provided and raise the proper errors
	"""
	if os.path.exists(os.path.join(_REPO_ROOT, str(args.year), f"Day {str(args.day)}")):
		raise ValueError(
			f"A project for the given day already exists: {str(args.year)}/Day {str(args.day)}"
		)


def _get_arguments(cmd_args: list = None) -> argparse.Namespace:
	"""
	Parses through the commandline arguments and returns the namespace with the
	parsed values.

	:return argparse.Namespace: Object containing the commandline arguments
	"""
	parser = argparse.ArgumentParser("{PROPER-NAME}")

	parser.add_argument(
		"--module-name", dest='module_name', type=str, required=True,
		help="Name of the project. EX: 'rucksack_reorganization'"
	)

	parser.add_argument(
		"--proper-name", dest='proper_name', type=str, required=True,
		help="Proper name of the project. EX: 'Rucksack Reorganization'"
	)

	parser.add_argument(
		"--day", dest='day', type=int, required=True,
		help="What day of the advent calendar is it. EX: 4"
	)

	parser.add_argument(
		"--year", dest='year', type=int, required=True,
		help="What year of Advent of Code it is. EX: 2022"
	)

	args = parser.parse_args() if cmd_args is None else parser.parse_args(cmd_args)
	_validate_arguments(args)

	return args


def main(cmd_args: list = None):
	"""
	Main function which will act as an entry point for this script.

	:param list cmd_args: Optional list of commandline arguments, defaults to None
	:return tuple[int,int]: (A, B)
	"""

	args = _get_arguments(cmd_args)
	_generate_project(args)


if __name__ == '__main__':
	main()
