'''
Module: region
Author: David Frye
Description: Contains the Region class.
'''

from utility import Direction

class Region:
	'''
	Class: Region
	Description: Represents a contiguous multidimensional range, called a "region".
	'''

	def __init__(self, position, size=None, endpoint=None):
		'''
		Method: __init__
		Description: Region constructor.
		Parameters: position, size=None, endpoint=None
			position: 2-Tuple - The position of the "lowest endpoint/corner" of the region from which each dimension grows by its respective size
			size: 2-Tuple - The size of the Region
			endpoint: 2-Tuple - The "highest endpoint/corner" of the region
		Return: None
		'''

		self.m_position = position

		if size:
			self.m_size = size
			self.m_range = ((position[0], position[0] + size[0] - 1), (position[1], position[1] + size[1] - 1))
			self.m_endpoint = (self.m_range[0][1], self.m_range[1][1])

		elif endpoint:
			self.m_size = (abs(endpoint[0] - position[0]), abs(endpoint[1] - position[1]))

			lower_endpoint = (min(position[0], endpoint[0]), min(position[1], endpoint[1]))
			upper_endpoint = (max(position[0], endpoint[0]), max(position[1], endpoint[1]))
			self.m_range = ((lower_endpoint[0], upper_endpoint[0]), (lower_endpoint[1], upper_endpoint[1]))

			self.m_endpoint = endpoint

		# To save memory, the set is not created until the first call to to_set, at which time it is stored within the Region object.
		self.m_set = None

	def contains(self, candidate_position):
		'''
		Method: contains
		Description: Determines whether or not the given candidate position is included in the region.
		Parameters: candidate_position
			candidate_position: 2-Tuple - The position to be checked for inclusion in the region
		Return: Boolean - Whether or not the candidate position is included in the region
		'''

		if candidate_position in self.to_set():
			return True
		else:
			return False

	def on_border(self, candidate_position):
		'''
		Method: on_border
		Description: Determines whether or not the given candidate position is sitting on/adjacent to an inside border of the region.
		Parameters: candidate_position, direction=None
			candidate_position: 2-Tuple - The position to be checked for adjacency to an inside border region
		Return: List - All of the borders that the given candidate position borders
		'''

		borders = []

		# If the candidate position is not contained in the region, it cannot be on the inside border of the region.
		if not self.contains(candidate_position):
			return borders

		# Check for adjacency to the northern border.
		if candidate_position[1] == self.m_range[1][0]:
			borders.append(Direction.NORTH)
		# Check for adjacency to the eastern border.
		if candidate_position[0] == self.m_range[0][1]:
			borders.append(Direction.EAST)
		# Check for adjacency to the southern border.
		if candidate_position[1] == self.m_range[1][1]:
			borders.append(Direction.SOUTH)
		# Check for adjacency to the western border.
		if candidate_position[0] == self.m_range[0][0]:
			borders.append(Direction.WEST)

		return borders

	def to_set(self):
		'''
		Method: to_set
		Description: Converts the region to a set of all points contained within the region.
		Parameters: No parameters
		Return: Set([2-Tuple]) - A set of all points contained within the region.
		'''

		if self.m_set is None:
			self.m_set = set([])
			for x in self.get_range_x():
				for y in self.get_range_y():
					self.m_set.add((x, y))

		return self.m_set

	def get_range_x(self):
		'''
		Method: get_range_x
		Description: Gets the x-dimensional range of the region.
		Parameters: No parameters
		Return: Range(x0, x1) - The x-dimensional range of the region
		'''

		return range(self.m_range[0][0], self.m_range[0][1] + 1)

	def get_range_y(self):
		'''
		Method: get_range_y
		Description: Gets the y-dimensional range of the region.
		Parameters: No parameters
		Return: Range(y0, y1) - The y-dimensional range of the region
		'''

		return range(self.m_range[1][0], self.m_range[1][1] + 1)