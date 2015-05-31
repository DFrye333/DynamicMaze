'''
Module: map
Author: David Frye
Description: Contains the Map class.
'''

import maze
import player

class Map:
	'''
	'''

	def __init__(self, maze=Maze(), player=Player()):
		'''
		'''

		self.m_maze = maze
		self.m_player = player