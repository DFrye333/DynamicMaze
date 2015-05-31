'''
Module: maze
Author: David Frye
Description: Contains the Maze class.
'''

import collections
import random
import time

from cell import Cell
from region import Region
from utility import Direction

class Maze:
	'''
	Class: Maze
	Description: Represents an individual maze, consisting of multiple cells.
	'''

	DEFAULT_WIDTH = 40
	DEFAULT_HEIGHT = 30
	DEFAULT_SCALE = 2
	DEFAULT_OPEN_CHANCE = 50

	def __init__(self, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT), scale=DEFAULT_SCALE):
		'''
		Method: __init__
		Description: Maze constructor
		Parameters: size=(DEFAULT_WIDTH, DEFAULT_HEIGHT), scale=DEFAULT_SCALE
			size: 2-Tuple - The dimensional lengths of the maze
				[0] - Maze x-dimensional length
				[1] - Maze y-dimensional length
			scale: The printing scale of the maze, used to determine spacing
		Return: None
		'''

		# The width/height of the maze.
		self.m_size = size
		# Scale must be an even number for proper pretty-printing.
		self.m_scale = 2 * scale
		# The individual cells of the maze.
		self.m_cells = [[Cell(Cell.UNVISITED_STRING, (x, y)) for x in range(self.get_width())] for y in range(self.get_height())]
		# A region representing the span of the maze.
		self.m_region = Region((0, 0), (self.get_width(), self.get_height()))

	def generate(self, region=None, exemptions=None, open_chance=DEFAULT_OPEN_CHANCE):
		'''
		Method: generate
		Description: Generate a maze within the provided bounds.
		Parameters: region=None, exemptions=None, open_chance=DEFAULT_OPEN_CHANCE
			region: Region - A region for maze generation to span
			exemptions: Regions - A collection of regions for maze generation to avoid
			open_chance: The percent chance that each cell will 
		Return: None
		'''

		# Ensure that valid boundaries are set.
		if region is None:
			region = Region((0, 0), (self.get_width(), self.get_height()))

		# Construct a set of valid cells.
		valid_cell = self.valid_cell_set(region, exemptions)

		# If there are no valid cells for generation, return.
		if not valid_cell:
			return

		# Randomly choose a starting cell from the valid cells.
		start_cell = random.sample(valid_cell, 1)[0]

		# Visit the starting cell and push it onto the cell stack.
		self.trailblaze(start_cell, None)
		cell_stack = [start_cell]

		# Crawl the entire maze.
		while cell_stack:

			# Grab the top cell from the cell stack.
			current_cell = cell_stack[-1]

			# Initialize the list of travel directions.
			directions = set([Direction(x) for x in range(0, 4)])
			while True:

				# If all directions have been tried, backtrack through the cell stack.
				if not directions:
					cell_stack.pop()
					break

				# Find a valid direction to trailblaze in.
				direction = random.sample(directions, 1)[0]

				# Attempt to trailblaze to the neighboring cell.
				target = self.trailblaze(current_cell, direction, region, exemptions)

				# If the trailblaze was successful, move on to the next cell, opening up the maze in the process if desired.
				if target is not None:

					# Add the next cell to the cell stack.
					cell_stack.append(target)

					# Open up the maze by plowing through walls at random.
					if random.randint(1, 100) <= open_chance:
						direction = random.sample(directions, 1)[0]
						if direction is not None:
							neighbor = self.get_neighbor_cell(current_cell, direction)
							if neighbor is not None and neighbor.is_visited():
								self.set_wall(current_cell, direction, False)

					break

				# If direction is invalid, remove it before trying again.
				directions.remove(direction)

	def trailblaze(self, source_cell, direction=None, region=None, exemptions=None):
		'''
		Method: trailblaze
		Description: Trailblaze from the source cell in the specified direction, knocking down both sides of the wall between the source and the target.
		Parameters: source_cell, direction=None, region=None, exemptions=None
			source_cell: Cell - The cell to trailblaze from
			direction: Direction - The direction to trailblaze in (None simply visits the source cell)
			region: Region - A region for trailblazing to span
			exemptions: Regions - A collection of regions for trailblazing to avoid
		Return: Cell - The target cell is trailblazing was successful, and None otherwise
		'''

		# If the direction is None, "trailblaze" to the source cell by marking it as visited.
		if direction is None:
			self.visit(source_cell)
			return source_cell

		# Ensure that valid boundaries are set.
		if region is None:
			region = Region((0, 0), (self.get_width(), self.get_height()))

		# Grab the target cell.
		target_cell = self.get_neighbor_cell(source_cell, direction)

		# If the target cell is invalid, return without trailblazing.
		if target_cell is None:
			return None

		# If the target cell is exempt, return without trailblazing.
		if exemptions is not None:
			for exemption in exemptions:
				if exemption.contains(target_cell.m_position):
					return None

		# If non-exempt target cell is valid, trailblaze to it.
		if not target_cell.is_visited() and region.contains(target_cell.m_position):

			# Remove wall between source and target cells.
			self.set_wall(source_cell, direction, False)

			# Visit the target cell.
			self.visit(target_cell)

			return target_cell

	def reset(self, region=None, exemptions=None):
		'''
		Method: reset
		Description: Reset cells inside the provided region whose coordinates do not also fall within any of the provided exemption ranges.
		Parameters: region=None, exemptions=None
			region: Region - A region for maze reset to span
			exemptions: Regions - A collection of regions for maze reset to avoid
		Return: None
		'''

		# Ensure that valid boundaries are set.
		if region is None:
			region = Region((0, 0), (self.get_width(), self.get_height()))

		# Reset all cells that do not fall inside any of the provided exempt ranges.
		for row in self.m_cells:

			# If the current row is inside the reset boundary, check for cells to reset inside that row.
			for cell in row:
				exempt = False

				# If the current cell is outside the reset boundary, move on to the next cell.
				if not region.contains(cell.m_position):
					continue

				# Check for the inclusion of each cell in each provided exempt range.
				if exemptions is not None:
					for exemption in exemptions:

						# Reset the boundary walls of the provided exempt ranges.
						border_directions = exemption.on_border(cell.m_position)
						for border_direction in border_directions:
							self.set_wall(cell, border_direction, True)

						# If the cell falls inside any of the provided exempt ranges, do not reset it.
						if exemption.contains(cell.m_position):
							exempt = True
							break

					# Do not reset exempt cells.
					if exempt:
						continue

				# Completely reset non-exempt cells.
				self.unvisit(cell)
				for direction in list(Direction):
					self.set_wall(cell, direction, True)

	def open(self, region=None, exemptions=None, open_border=True):
		'''
		Method: open
		Description: Opens (visits all cells and destroys all walls within) the given region, avoiding the given exempt regions.
		Parameters: region=None, exemptions=None
			region: Region - A region for maze opening to span
			exemptions: Regions - A collection of regions for maze opening to avoid
		Return: None
		'''

		# Ensure that valid boundaries are set.
		if region is None:
			region = Region((0, 0), (self.get_width(), self.get_height()))

		# Construct a set of valid cells.
		valid_cells = self.valid_cell_set(region, exemptions)

		# Visit all valid cells and open the walls as necessary (region borders only open if open_border is True).
		for cell in valid_cells:
			cell.visit()
			border_directions = region.on_border(cell.m_position)
			for direction in list(Direction):

				# Ensure that the border is allowed to be destroyed.
				if (self.get_neighbor_cell(cell, direction) is not None) and (open_border) or (direction not in border_directions):
					self.set_wall(cell, direction, False)


	def solve(self, start_cell_position, end_cell_position, breadcrumbs=False):
		'''
		Method: solve
		Description: Finds a path between the given start and end cells.
		Parameters: start_cell_position, end_cell_position, breadcrumbs=False
			start_cell_position: 2-Tuple - The cell position to begin searching from
			end_cell_position: 2-Tuple - The cell position to target in the search
			breadcrumbs: Boolean - Whether or not to change the content of cells along the solution path for pretty-printing
		Return: [Cell] - A list of cells denoting the solution path, or None if no solution is found
		'''

		# Reset any residual solution breadcrumb trails.
		for row in self.m_cells:
			for cell in row:
				if self.get_cell_content(cell.m_position) == "*":
					self.set_cell_content(cell.m_position, " ")

		# If the start and end positions are the same, return the one cell as the entire solution path list.
		if start_cell_position == end_cell_position:
			return [start_cell_position]

		# Ensure that the starting cell position is a valid cell.
		start_cell = self.get_cell(start_cell_position)
		if start_cell is None:
			return None

		# Enqueue the starting cell into the cell queue.
		cell_queue = collections.deque([start_cell])
		# Maintain traversal pathways throughout the maze.
		pathways = {}

		# Crawl the entire maze for as long as the end cell is not found.
		while cell_queue:

			# Grab the first cell from the cell queue.
			current_cell = cell_queue.popleft()

			# If the end cell has been found, perform a backtrace and return the solution path.
			if current_cell.m_position == end_cell_position:

				final_pathway = []

				# Backtrace to the starting cell.
				while current_cell.m_position != start_cell_position:

					# Add the current cell to the final pathway.
					final_pathway.append(current_cell)

					# Backtrace to the previous cell.
					current_cell = pathways[current_cell]

				# Add the starting cell to the final pathway.
				final_pathway.append(current_cell)

				# Reverse the pathway due to its formation during backtracing.
				final_pathway.reverse()

				# If breadcrumbs are enabled, leave breadcrumbs along the final pathway.
				if breadcrumbs:
					for cell in final_pathway:
						cell.set_content("*")

				return final_pathway

			# Add all accessible neighbor cells to the cell queue.
			accessible_neighbors = self.get_accessible_neighbor_cells(current_cell)
			for neighbor in accessible_neighbors:
				if (neighbor is not None) and (neighbor not in pathways):
					cell_queue.append(neighbor)
					pathways[neighbor] = current_cell

	def print_maze(self):
		'''
		Method: print_maze
		Description: Pretty-prints the maze to a file.
		Parameters: No parameters
		Return: None
		'''

		with open("maze.txt", "w") as outfile:
			# Print maze header.
			outfile.write("Maze (" + str(self.get_width()) + " x " + str(self.get_height()) + "):\n")
			for row in self.m_cells:
				# Print the rows between the cells.
				for cell in row:
					outfile.write(Cell.WALL_VERTICAL_STRING) if cell.m_walls.get(Direction.WEST) else outfile.write(Cell.WALL_HORIZONTAL_STRING)
					outfile.write(self.m_scale * Cell.WALL_HORIZONTAL_STRING) if cell.m_walls.get(Direction.NORTH) else outfile.write(self.m_scale * " ")
				outfile.write(Cell.WALL_VERTICAL_STRING)
				outfile.write("\n")
				# Print the rows containing the cells.
				for cell in row:
					outfile.write(Cell.WALL_VERTICAL_STRING + " ") if cell.m_walls.get(Direction.WEST) else outfile.write("  ")
					outfile.write((((self.m_scale - 1) // 2) * " ") + cell.m_content + (((self.m_scale - 1) // 2) * " "))
				outfile.write(Cell.WALL_VERTICAL_STRING)
				outfile.write("\n")
			# Print bottom maze border.
			outfile.write(Cell.WALL_VERTICAL_STRING + (((self.m_scale + 1) * self.get_width() - 1) * Cell.WALL_HORIZONTAL_STRING) + Cell.WALL_VERTICAL_STRING + "\n")

	def visit(self, cell):
		'''
		Method: visit
		Description: Sets the given cell into a visited state.
		Parameters: cell
			cell: Cell - The cell being visited
		Return: None
		'''

		try:
			cell.visit()
		except AttributeError as e:
			print(e)

	def unvisit(self, cell):
		'''
		Method: unvisit
		Description: Sets the given cell into an unvisited state.
		Parameters: cell
			cell: Cell - The cell being unvisited
		Return: None
		'''

		try:
			cell.unvisit()
		except AttributeError as e:
			print(e)

	def direction_to_offset(self, direction):
		'''
		Method: direction_to_offset
		Description: Converts a Direction to a cell offset.
		Parameters: direction
			direction: Direction - The direction to convert into an offset
		Return: 2-Tuple - An offset in a given direction
			[0] = The x-dimensional offset
			[1] = The y-dimensional offset
		'''

		if direction == Direction.NORTH:
			return (0, -1)
		elif direction == Direction.EAST:
			return (1, 0)
		elif direction == Direction.SOUTH:
			return (0, 1)
		elif direction == Direction.WEST:
			return (-1, 0)
		else:
			return (0, 0)

	def is_valid_cell_position(self, position):
		'''
		Method: is_valid_cell_position
		Description: Determines whether the given position is a valid cell within the maze.
		Parameters: position
			position: 2-Tuple - A position value
				[0] = The x-position
				[1] = The y-position
		Return: Boolean - Whether or not the given position is a valid cell within the maze
		'''

		if position in self.m_region.to_set():
			return True
		else:
			return False

	def valid_cell_set(self, region, exemptions):
		'''
		Method: valid_cell_set
		Description: Constructs a set of valid cells (cells that are in the intersection of the maze cell set and the region cell set, subtracting those in the exempt region sets).
		Parameters: region, exemptions
			region: Region - A region of cells to intersect with the cells of the maze
			exemptions: Regions - A collection of regions to subtract from the valid cell set
		Return: Set([Cell]) - A set of valid cells (cells that are in the intersection of the maze cell set and the region cell set, subtracting those in the exempt region sets)
		'''

		valid_cell_positions = self.m_region.to_set() & region.to_set()
		if exemptions is not None:
			for exemption in exemptions:
				valid_cell_positions -= exemption.to_set()

		return set([self.get_cell(x) for x in valid_cell_positions])

	def get_accessible_neighbor_cells(self, source_cell):
		'''
		Method: get_accessible_neighbor_cells
		Description: Gets a list of all neighboring cells which are directly-accessible from the given source cell.
		Parameters: source_cell
			source_cell: Cell - The cell to check the neighbors of
		Return: [Cell] - All neighboring cells directly-accessible from the given source cell
		'''

		accessible_neighbor_cells = []

		for direction in list(Direction):
			if not source_cell.get_wall(direction):
				accessible_neighbor_cells.append(self.get_neighbor_cell(source_cell, direction))

		return accessible_neighbor_cells

	def get_neighbor_cell(self, source_cell, direction):
		'''
		Method: get_neighbor_cell
		Description: Gets the cell neighboring the given source cell in the given direction.
		Parameters: source_cell, direction
			source_cell: Cell - The cell neighboring the target
			direction: Direction - The direction to grab from the source cell
		Return: Cell - The cell neighboring the given source cell in the given direction
		'''

		neighbor_offset = self.direction_to_offset(direction)
		return self.get_cell((source_cell.get_position_x() + neighbor_offset[0], source_cell.get_position_y() + neighbor_offset[1]))

	def get_cell(self, position):
		'''
		Method: get_cell
		Description: Gets the Cell at a given position, transposing column-major positional input into row-major positional input.
		Parameters: position
			position: 2-Tuple - A position value
				[0] = The x-position
				[1] = The y-position
		Return: Cell - The Cell at a given position
		'''

		if self.is_valid_cell_position(position):
			return self.m_cells[position[1]][position[0]]
		else:
			return None

	def get_cell_content(self, position):
		'''
		Method: get_cell_content
		Description: Gets the cell_content of the given cell.
		Parameters: position
			position: 2-Tuple - A position value
				[0] = The x-position
				[1] = The y-position
		Return: String - A string visually representing the cell
		'''

		return self.get_cell(position).get_content()

	def get_height(self):
		'''
		Method: get_height
		Description: Gets the height of the maze.
		Parameters: No parameters
		Return: Int - The maze height
		'''

		return self.m_size[1]

	def get_wall(self, source_cell, direction):
		'''
		Method: get_wall
		Description: Modify both sides of a given cell's wall in a given direction by a given value.
		Parameters: source_cell, direction
			source_cell: Cell - The cell whose wall is to be retrieved
			direction: Direction - The direction of the wall to be retrieved
		Return: Boolean - Whether the wall exists or not
		'''

		return source_cell.get_wall(direction)

	def get_width(self):
		'''
		Method: get_width
		Description: Gets the width of the maze.
		Parameters: No parameters
		Return: Int - The maze width
		'''

		return self.m_size[0]

	def set_cell_content(self, position, value):
		'''
		Method: set_cell_content
		Description: Sets the cell content of the given cell.
		Parameters: position, value
			position: 2-Tuple - A position value
				[0] = The x-position
				[1] = The y-position
			value: String - A string visually representing the cell
		Return: None
		'''

		self.get_cell(position).set_content(value)

	def set_height(self, height):
		'''
		Method: set_height
		Description: Sets the height of the maze.
		Parameters: height
			height: Int - The maze height
		Return: None
		'''

		self.m_size[1] = height

	def set_wall(self, source_cell, direction, value):
		'''
		Method: set_wall
		Description: Modify both sides of a given cell's wall in a given direction by a given value.
		Parameters: source_cell, direction, value
			source_cell: Cell - The cell whose wall is to be set
			direction: Direction - The direction of the wall to be set
			value: Boolean - Whether the wall should exist or not
		Return: None
		'''

		# Modify wall on the given source_cell's side.
		if self.is_valid_cell_position(source_cell.m_position):
			source_cell.set_wall(direction, value)

		# Modify shared wall of the neighbor cell in the given direction.
		neighbor_cell = self.get_neighbor_cell(source_cell, direction)
		if neighbor_cell is not None and self.is_valid_cell_position(neighbor_cell.m_position):
			neighbor_cell.set_wall(Direction.get_opposite(direction), value)

	def set_width(self, width):
		'''
		Method: set_width
		Description: Sets the width of the maze.
		Parameters: width
			width: Int - The maze width
		Return: None
		'''

		self.m_size[0] = width