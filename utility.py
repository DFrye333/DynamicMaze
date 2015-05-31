'''
Module: utility
Author: David Frye
Description: Contains a variety of helper Classes.
'''

import enum
import random

class Direction(enum.Enum):
	'''
	Enum: Direction
	Description: Represents the four primary cardinal directions (North, East, South, and West)
	'''
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	def get_random():
		'''
		Method: get_random_direction
		Description: Gets a random direction from the available directions
		Parameters: No Parameters
		Return: Direction - A random direction from the available directions
		'''

		return Direction(random.randint(0, 3))

	def get_opposite(direction):
		'''
		Method: get_opposite_direction
		Description: Gets the direction opposite to the one given
		Parameters: direction
			direction: Direction - The direction to get the opposite direction of
		Return: Direction - The direction opposite to the one given
		'''

		return Direction((direction.value + 2) % 4)

	def get_next_clockwise(direction):
		'''
		Method: get_next_clockwise
		Description: Get the direction next to the given direction via a clockwise rotation.
		Parameters: direction
			direction: Direction - The value to rotate from
		Return: Direction - The direction next to the given direction via a clockwise rotation
		'''

		return Direction((direction.value + 1) % 4)

	def get_next_counterclockwise(direction):
		'''
		Method: get_next_counterclockwise
		Description: Get the direction next to the given direction via a counterclockwise rotation.
		Parameters: direction
			direction: Direction - The value to rotate from
		Return: Direction - The direction next to the given direction via a counterclockwise rotation
		'''

		return Direction((direction.value - 1) % 4)

def pause():
	input("Paused! Press 'Enter' to continue...")