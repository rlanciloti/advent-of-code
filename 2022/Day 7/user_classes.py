"""
This file will contain the classes used in teh no_space.py script
"""
from __future__ import annotations
from typing import Union
from dataclasses import dataclass


@dataclass
class File:
	"""
	File: Represents a file
	"""
	def __init__(self, name: str, size: int):
		"""
		Constructor for the File class

		:param str name: Name of the file
		:param int size: Size of the file
		"""
		self.name: str = name
		self.size: int = size


class Directory:
	"""
	Directory: Represents a directory
	"""

	def __init__(self, name: str):
		"""
		Constructor for the Directory class
		:param str name: Name of the directory
		"""
		self.name: str = name
		self._contents: list = []
		self._size: int = 0
		self._updated: bool = False

	@property
	def size(self) -> int:
		"""
		Returns the total size of a given directory

		:return int: Size of the directory
		"""
		if not self._updated:
			return self._size

		size = 0

		for item in self._contents:
			size += item.size

		self._size = size
		self._updated = False
		return size

	def get(self, dir_name: str) -> Directory:
		"""
		Returns a reference to a subdirectory in the current directory of a given name

		:param str dir_name: Name of the directory to return
		:return Directory: Reference to the directory with a given name
		"""
		for item in self._contents:
			if isinstance(item, Directory) and item.name == dir_name:
				return item

		raise ValueError(
			"No directory of the given name found in the current directory.\n"
			f"Current Directory: {self.name}"
			f"Requested Directory: {dir_name}"
		)

	def add(self, item: Union[Directory, File]):
		"""
		This function adds a given item to the contents list

		:param Union[Directory, File] item: Item to be added to the contents list
		"""
		self._contents.append(item)
		self._updated = True
