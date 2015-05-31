'''
Module: test
Author: David Frye
Description: Tests the dynamically-mutating maze program. A prototype for Labyrinthine.
'''

import time

from maze import Maze
from region import Region
from utility import Direction
from utility import pause

def test_0():
	width = 40
	height = 30
	scale = 2

	maze = Maze((width, height), scale)
	maze.generate()
	maze.print_maze()

def test_1():
	width = 40
	height = 30
	scale = 2

	exemptions = (
		Region(((width // 2) - 5, (height // 2) - 5), (10, 10)),
		Region((0, 0), (3, 5)))

	maze = Maze((width, height), scale)
	maze.generate()
	maze.print_maze()
	utility.pause()
	maze.reset(Region((0, 0), (width, (3 * height) // 4)), exemptions)
	maze.print_maze()
	utility.pause()
	maze.generate(Region((width - 5, 0), (5, 5)))
	maze.print_maze()
	utility.pause()
	maze.reset()
	maze.generate()
	maze.print_maze()

def test_2():
	width = 30
	height = 30
	scale = 2

	maze = Maze((width, height), scale)
	maze.generate(Region((0, 0), (5, 5)))
	maze.generate(Region((5, 0), (5, 5)))
	maze.set_wall(maze.get_cell((4, 4)), Direction.EAST, False)
	maze.print_maze()

def test_3():
	width = 40
	height = 10000
	scale = 2

	maze = Maze((width, height), scale)
	maze.generate()
	maze.print_maze()

def test_4():
	width = 40
	height = 15
	scale = 2

	maze = Maze((width, height), scale)
	maze.generate(Region((5, 2), (95, 98)))
	maze.print_maze()

def test_5():
	maze = Maze()
	width = maze.get_width()
	height = maze.get_height()

	maze.generate(Region((0, 0), endpoint=(width // 2, height // 2)))
	maze.generate(Region((width // 2, 0), endpoint=(width, height // 2)))
	maze.generate(Region((0, height // 2), endpoint=(width // 2, height)))
	maze.generate(Region((width // 2, height // 2), endpoint=(width, height)))
	maze.print_maze()
	utility.pause()
	maze.reset(Region((0, 0), (width // 2, height // 2)))
	maze.generate(Region((0, 0), (width // 2, height // 2)))
	maze.print_maze()

def test_6():
	maze = Maze()
	width = maze.get_width()
	height = maze.get_height()

	maze.generate(Region((width // 4, height // 4), endpoint=(width // 2, height // 2)))
	maze.print_maze()

def test_7():
	maze = Maze()
	width = maze.get_width()
	height = maze.get_height()

	maze.generate(Region(position=(0, 0), size=(width, height)), (Region(position=(1, height // 2), size=(width - 2, 1)), Region(position=(width // 2, 1), size=(1, height - 2))))
	maze.print_maze()

def test_8():
	maze = Maze(size=(40, 1000))

	time1 = time.clock()
	maze.generate()
	time2 = time.clock()
	print("Generated in:", time2 - time1, "seconds.")
	time1 = time.clock()
	maze.solve((maze.get_width() // 2, maze.get_height() // 2), (maze.get_width() - 1, maze.get_height() - 1), True)
	time2 = time.clock()
	print("Solved in:", time2 - time1, "seconds.")
	maze.print_maze()

def test_9():
	maze = Maze()
	width = maze.get_width()
	height = maze.get_height()
	start = (0, height - 1)
	end = (width - 1, height - 1)

	maze.generate(exemptions=((Region((width // 2, 1), (1, height - 1)), )))
	maze.print_maze()
	maze.solve(start, end, True)
	maze.print_maze()

def test_10():
	time1 = time.clock()

	time11 = time.clock()
	width = 20
	height = 20
	center = ((width // 2) - 1, (height // 2) - 1)
	generate_regions = (
		Region((0, 0), endpoint=center),
		Region((0, height - 1), endpoint=center),
		Region((width - 1, 0), endpoint=center),
		Region((width - 1, height - 1), endpoint=center))
	exempt_regions = (
		Region((0, 0), endpoint=(1, 1)),
		Region((0, height - 1), endpoint=(1, height - 2)),
		Region((width - 1, 0), endpoint=(width - 2, 1)),
		Region((width - 1, height - 1), endpoint=(width - 2, height - 2)),
		Region(center, size=(2, 2)))

	maze = Maze(size=(width, height))
	time12 = time.clock()

	time3 = time.clock()
	for i in range(0, 4):
		maze.generate(generate_regions[i], exempt_regions)
	time4 = time.clock()

	time5 = time.clock()
	for exempt_region in exempt_regions:
		maze.open(exempt_region)
	time6 = time.clock()

	time7 = time.clock()
	for exempt_region in exempt_regions:
		for cell_position in exempt_region.to_set():
			maze.get_cell(cell_position).set_content("H")
	time8 = time.clock()

	time9 = time.clock()
	maze.solve((0, 0), (width - 1, height - 1), True)
	time10 = time.clock()

	time13 = time.clock()
	maze.print_maze()
	time14 = time.clock()

	time2 = time.clock()

	time_total = time2 - time1
	time_generate = time4 - time3
	time_open = time6 - time5
	time_set = time8 - time7
	time_solve = time10 - time9
	time_init = time12 - time11
	time_print = time14 - time13

	print()
	print("Completed the ", width * height, "-cell maze in: ", round(time_total, 2), " seconds.", sep="")
	print("\tGenerate: ", round((time_generate) / (time_total) * 100), "%", sep="")
	print("\tOpen: ", round((time_open) / (time_total) * 100), "%", sep="")
	print("\tSet: ", round((time_set) / (time_total) * 100), "%", sep="")
	print("\tSolve: ", round((time_solve) / (time_total) * 100), "%", sep="")
	print("\tInit: ", round((time_init) / (time_total) * 100), "%", sep="")
	print("\tPrint: ", round((time_print) / (time_total) * 100), "%", sep="")
	print()

def test_11():
	width = 40
	height = 30
	center = ((width // 2) - 1, (height // 2) - 1)
	generate_regions = (
		Region((0, 0), endpoint=center),
		Region((0, height - 1), endpoint=(center[0], center[1] + 1)),
		Region((width - 1, 0), endpoint=(center[0] + 1, center[1])),
		Region((width - 1, height - 1), endpoint=(center[0] + 1, center[1] + 1)))
	exempt_regions = (
		Region((0, 0), endpoint=(1, 1)),
		Region((0, height - 1), endpoint=(1, height - 2)),
		Region((width - 1, 0), endpoint=(width - 2, 1)),
		Region((width - 1, height - 1), endpoint=(width - 2, height - 2)),
		Region(center, size=(2, 2)))

	maze = Maze(size=(width, height))

	for i in range(0, 4):
		maze.generate(generate_regions[i], exempt_regions)

	for exempt_region in exempt_regions:
		maze.open(exempt_region)

	for exempt_region in exempt_regions:
		for cell_position in exempt_region.to_set():
			maze.get_cell(cell_position).set_content("H")

	count = 0
	while True:
		time1 = time.clock()
		solved1 = maze.solve((0, 0), (width - 1, height - 1), True)
		# solved2 = maze.solve((0, height - 1), center, True)
		# solved3 = maze.solve((width - 1, 0), center, True)
		# solved4 = maze.solve((width - 1, height - 1), center, True)
		time2 = time.clock()

		
		if (not solved1):# or (not solved2) or (not solved3) or (not solved4):
			print("Fail...")
			maze.print_maze()
			utility.pause()
		else:
			print("Solved in", round(time2 - time1, 2), "!")

		maze.print_maze()
		time.sleep(2)

		maze.reset(generate_regions[count % 4])
		maze.generate(generate_regions[count % 4], exempt_regions, open_chance=100)

		for exempt_region in exempt_regions:
			maze.open(exempt_region)

		for exempt_region in exempt_regions:
			for cell_position in exempt_region.to_set():
				maze.get_cell(cell_position).set_content("H")

		count += 1

def test_miscellaneous():
	region = Region((0, 5), (10, 15))
	print(region.m_range)
	print(region.contains((0, 5)))
	print(region.contains((10, 10)))
	print(region.contains((0, 21)))
	print(region.get_endpoints())
	print(region.on_border((9, 10)))

	maze = Maze()

	maze.generate(region=3)

def test_run():
	maze = Maze()
	player = Region((0, 0), endpoint=(5, 5))
	maze.generate(player)
	maze.get_cell(player.m_position).m_content = "P"

	while True:
		maze.print_maze()
		print("Updating")
		maze.get_cell(player.m_position).m_content = "*"
		maze.reset(player)

		new_x = player.m_position[0]
		new_y = player.m_position[1]
		if (player.m_position[0] + 1) >= maze.get_width():
			new_x = 0
			if (player.m_position[1] + 1 >= maze.get_height()):
				new_y = 0
			else:
				new_y += 1
		else:
			new_x += 1
		player = Region((new_x, new_y), player.m_size)
		maze.generate(player)
		maze.get_cell(player.m_position).m_content = "P"

		time.sleep(1)

def test_harness():
	user_input_prompt = "Test: "

	user_input = str(input(user_input_prompt))
	while user_input != "":
		if user_input == "0":
			test_0()
		elif user_input == "1":
			test_1()
		elif user_input == "2":
			test_2()
		elif user_input == "3":
			test_3()
		elif user_input == "4":
			test_4()
		elif user_input == "5":
			test_5()
		elif user_input == "6":
			test_6()
		elif user_input == "7":
			test_7()
		elif user_input == "8":
			test_8()
		elif user_input == "9":
			test_9()
		elif user_input == "10":
			test_10()
		elif user_input == "11":
			test_11()
		elif user_input == "m":
			test_miscellaneous()
		elif user_input == "r":
			test_run()
		else:
			print("Unknown input!")

		user_input = input(user_input_prompt)