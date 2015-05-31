'''
Module: cell
Author: David Frye
Description: Contains the Cell class.
'''

from utility import Direction

class Cell:
	'''
	Class: Cell
	Description: Represents an individual cell in a maze.
	'''

	# The print character for a visited cell.
	VISITED_STRING = " "
	# The print character for an unvisited cell.
	UNVISITED_STRING = "/"
	# The print character for a horizontal wall.
	WALL_HORIZONTAL_STRING = "-"
	# The print character for a vertical wall.
	WALL_VERTICAL_STRING = "|"

	def __init__(self, content, position):
		'''
		Method: __init__
		Description: Cell constructor.
		Parameters: content, position
			content: String - A string visually representing the cell
			position: 2-Tuple - The cell's position in the maze that owns it
				[0] - Cell's x-position
				[1] - Cell's y-position
		Return: None
		'''

		self.m_content = content
		self.m_position = position
		self.m_visited = False
		self.m_walls = {
			Direction.NORTH : True,
			Direction.EAST : True,
			Direction.SOUTH : True,
			Direction.WEST : True
		}

	def visit(self):
		'''
		Method: visit
		Description: Sets the cell's content attribute into the visited state.
		Parameters: No parameters
		Return: None
		'''

		self.m_visited = True
		self.m_content = self.VISITED_STRING

	def unvisit(self):
		'''
		Method: visit
		Description: Sets the cell's content attribute into the unvisited state.
		Parameters: No parameters
		Return: None
		'''

		self.m_visited = False
		self.m_content = self.UNVISITED_STRING

	def is_visited(self):
		'''
		Method: is_visited
		Description: Determines whether or not the cell is in the visited state.
		Parameters: No parameters
		Return: Boolean - Whether or not the cell is in the visited state
		'''

		return self.m_visited

	def get_content(self):
		'''
		Method: get_content
		Description: Gets the cell's content attribute.
		Parameters: No parameters
		Return: String - Cell's content attribute
		'''

		return self.m_content

	def get_position_x(self):
		'''
		Method: get_position_x
		Description: Gets the cell's x-position attribute.
		Parameters: No parameters
		Return: String - Cell's x-position attribute
		'''

		return self.m_position[0]

	def get_position_y(self):
		'''
		Method: get_position_y
		Description: Gets the cell's y-position attribute.
		Parameters: No parameters
		Return: String - Cell's y-position attribute
		'''

		return self.m_position[1]

	def get_wall(self, direction):
		'''
		Method: get_wall
		Description: Gets the cell's wall attribute corresponding to the given direction.
		Parameters: direction
			direction: Direction - Direction corresponding to the desired wall
		Return: String - Cell's wall attribute corresponding to the given direction
		'''

		return self.m_walls.get(direction)

	def set_content(self, content):
		'''
		Method: set_content
		Description: Sets the cell's content attribute.
		Parameters: content
			content: String - A string visually representing the cell
		Return: None
		'''

		self.m_content = content

	def set_position_x(self, x):
		'''
		Method: set_position_x
		Description: Sets the cell's x-position attribute.
		Parameters: x
			x: Int - Cell's x-position within the maze that owns it
		Return: None
		'''

		self.m_position[0] = x

	def set_position_y(self, y):
		'''
		Method: set_position_y
		Description: Sets the cell's y-position attribute.
		Parameters: y
			y: Int - Cell's y-position within the maze that owns it
		Return: None
		'''

		self.m_position[1] = y

	def set_wall(self, direction, value):
		'''
		Method: set_wall
		Description: Sets the cell's wall attribute corresponding to the given direction.
		Parameters: direction, value
			direction: Direction - Direction corresponding to the desired wall
			value: Boolean - Whether the wall exists or not
		Return: None
		'''

		self.m_walls[direction] = value