"""
This file will contain the unit tests for the calorie counting challenge

Author: Ryan Lanciloti
Date of Creation: 12/3/2022
"""
import os
from typing import List

import pytest
from .calorie_counting import main

_CUR_DIR_PATH = os.path.dirname(__file__)


def _build_test_suite() -> List[tuple]:
	"""
	This function will dynamically build a list of inputs and outputs for the testing framework

	:return List[tuple]: List of input and output files
	"""
	test_inputs_path = os.path.join(_CUR_DIR_PATH, "test_inputs")
	test_outputs_path = os.path.join(_CUR_DIR_PATH, "test_outputs")

	assert os.path.exists(test_inputs_path) and os.path.isdir(test_inputs_path), \
		"No \'test_inputs\' directory exists in the current directory."
	assert os.path.exists(test_outputs_path) and os.path.isdir(test_outputs_path), \
		"No \'test_outputs\' directory exists in the current directory."

	input_files = [
		os.path.join(test_inputs_path, file) for file in os.listdir(test_inputs_path)
		if os.path.isfile(os.path.join(test_inputs_path, file)) and file.startswith("test_input")
	]

	output_files = [
		os.path.join(test_outputs_path, file) for file in os.listdir(test_outputs_path)
		if os.path.isfile(os.path.join(test_outputs_path, file)) and file.startswith("test_output")
	]

	assert len(input_files) == len(output_files), \
		"There are a different number of input files compared to output files"

	input_files.sort()
	output_files.sort()

	return list(zip(input_files, output_files))


@pytest.mark.parametrize("infile, outfile", _build_test_suite())
def test_inputs(infile, outfile):
	"""
	This function will verify that the expected input matches the expected output
	"""
	with open(outfile, "r") as fptr:
		expected_output = fptr.read()

	actual_output = main(['--infile', infile])

	assert expected_output == str(actual_output), \
		f"Expected: {expected_output} does not match actual: {str(actual_output)}"
