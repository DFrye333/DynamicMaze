'''
Module: main
Author: David Frye
Description: Generates a dynamically-mutating maze. A prototype for Labyrinthine.
'''

import test

def run():
	return

def main():
	user_input_prompt = "Main menu: "

	user_input = str(input(user_input_prompt))
	while user_input != "":
		if user_input == "0":
			test.test_harness()
		elif user_input == "1":
			run()

		user_input = input(user_input_prompt)

main()