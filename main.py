import msvcrt
import os, sys, inspect
import time
import pickle
import minewalker
import cursor
import pickle
cursor.hide()

# Simple class that stores ANSI Escape characters for specific colours
class color:
	BOLD = '\u001b[1m'
	UNDERLINE = '\u001b[4m'
	SELECT = '\033[47m'
	BASE = '\033[0m'
	RED = '\033[91m'
	YELLOW = ''
	BLACK = '\033[30m'
	GREEN = '\033[92m'



#Main menu UI object
class UI(object):

	def __init__(self):
		self.keylog = []
		self.menulist = ["Play","Instructions","Leaderboard","Settings","Credits","Exit"]
		self.functionlist = ["Play","Instructions","Leaderboard","Settings","Credits","Exit"]
		self.currentSelection = 0
		self.mygame = minewalker.Game()
		self.highscores = {0:"Null",1:"Null",2:"Null",3:"Null",4:"Null",5:"Null"}
		self.highscoreNames = [] 
		self.highscoreList = []		
		self.load_leaderboard()
		self.reorganise_hs()

	def load_leaderboard(self):
		try:
			with open("highscores.dat","rb") as save:
				# Highscore dictionary
				self.highscores = pickle.load(save)
		except:
			pass
	
	def reorganise_hs(self):
		for score, name in sorted(self.highscores.items()):
			self.highscoreNames.append(name)
			self.highscoreList.append(score)
		self.highscoreList.reverse()
		self.highscoreNames.reverse()

	def check_highscore(self, score):
		# print(self.highscoreList)
		if score > self.highscoreList[3]:
			return True
		else:
			return False

	def save_highscore(self):
		with open("highscores.dat","wb") as sav:
			pickle.dump(self.highscores,sav)

	# Functions for each of the menu items
	def cls(self, type = 0):
		os.system("cls")

	def wait(self):
		while True:
			if msvcrt.kbhit():
				msvcrt.getch()
				return 0

	def save_to_disk(self,characterList):
		with open('settings.dat','wb') as save:
			pickle.dump(characterList, save)

	def load_settings(self):
		try:
			with open('settings.dat','rb') as save:
				characterList = pickle.load(save)
				self.mygame.playerChar = characterList[0]
				self.mygame.mineChar = characterList[1]
				self.mygame.pathChar = characterList[2]
				self.mygame.boxChar	= characterList[3]			
		except:
			pass

	# Main play function
	def play(self):
		self.load_settings()
		self.cls()
		word = "Difficulty:"
		width= os.get_terminal_size().columns
		half = width/2
		for listIndex, option in enumerate(word):
			blankchars = half - len(word)/2
			chars = ""
			for x in range(int(blankchars)):
				chars += " "
		print(chars + color.UNDERLINE + word + color.BASE)

		modes = ["Beginner", "Easy", "Normal", "Moderate", "Hard", "Extreme", "Ultra Madness"]
		self.print_list(modes,cls=False)

		if self.move_list(modes,cls=False) == 0:

			self.mygame.length = 10
			self.mygame.nMines = 15
			self.mygame.displayInterval = 2
			self.mygame.powerups = 100

			if self.currentSelection == 0:
				self.mygame.powerups = 30
				self.mygame.displayInterval = 2.5
				self.mygame.length = 10
				self.mygame.nMines = 15

			elif self.currentSelection == 1:
				self.mygame.displayInterval = 2.0
				self.mygame.powerups = 25
				self.mygame.length = 12
				self.mygame.nMines = 17

			elif self.currentSelection == 2:
				self.mygame.powerups = 20
				self.mygame.displayInterval = 1.5
				self.mygame.length = 14
				self.mygame.nMines = 20

			elif self.currentSelection == 3:
				self.mygame.length = 16
				self.mygame.powerups = 15
				self.mygame.displayInterval = 1.2
				self.mygame.nMines = 25

			elif self.currentSelection == 4:
				self.mygame.length = 18
				self.mygame.powerups = 10
				self.mygame.displayInterval = 1.0
				self.mygame.nMines = 30
			
			elif self.currentSelection == 5:
				self.mygame.length = 20
				self.mygame.powerups = 8
				self.mygame.displayInterval = 0.8
				self.mygame.nMines = 40

			elif self.currentSelection == 6:
				self.mygame.length = 22
				self.mygame.powerups = 5
				self.mygame.displayInterval = 0.5
				self.mygame.nMines = 60
			else:
				pass

		self.mygame.run()
		score = self.mygame.score
		if self.check_highscore(score) == True:
			print("You got a High Score!")
			name = str(input("Enter your Name: "))
			self.highscores[score] = name
			self.reorganise_hs()

		print("\nWould you like to Play Again?")
		option_list = ["Yes", "No"]
		print("\n")
		self.currentSelection = 0
		self.print_list(option_list,cls=False)
		if self.move_list(option_list,cls=False) == 0:
			if self.currentSelection == 0:
				self.cls()
				self.play()
				return 0 
			else:
				self.cls()
				return 0
		
	# Instructions function
	def instructions(self):
		# self.cls()
		instructions = """Welcome to MineWalker!\n\n{0}Objective:{1}
		\nReach the last square of the minefield without setting off any mines.\n
		\n{2}How to Play:{3}
		\nThe position of each mine will be shown to you for a small amount of time depending on your level of difficulty.
		\nRemember where the mines are and navigate the minefield using W A S D or the ARROW KEYS to get to the cell at the intersection of the last row and column.\n
		\n{4}Special Abilities:{5}
		\nQ --> Scan for mines in immediate squares around you
		""".format(color.UNDERLINE, color.BASE, color.UNDERLINE, color.BASE, color.UNDERLINE, color.BASE)
		print(instructions)
		print("\n\n[ Press ANY KEY to Return to Main Menu ]")
		self.wait()
		return 0

	# Leaderboard function
	def leaderboard(self):
		self.reorganise_hs()
		self.highscoreNames=self.highscoreNames[:4]
		self.highscoreList=self.highscoreList[:4]
		for iterator in range(len(self.highscoreNames)):
			print(str(self.highscoreNames[iterator]) + ": " + str(self.highscoreList[iterator]))
		print("\n\n[ Press ANY KEY to Return to Main Menu ]")
		self.wait()
		return 0
	# Settings function
	def settings(self):
		self.currentSelection = 0

		playerChar = self.mygame.playerChar
		mineChar = self.mygame.mineChar
		pathChar = self.mygame.pathChar
		boxChar = self.mygame.boxChar	

		menulist = [f"Choose your player character: {playerChar}", f"Choose your mine character: {mineChar}", f"Choose your path character: {pathChar}",
		f"Choose your box character: {boxChar}", "Save Changes", "Reset to Defaults", "Return to Main Menu"]
		self.print_list(menulist)
		# select = True
		characterList = [playerChar, mineChar, pathChar, boxChar]
		gameCharList = [self.mygame.playerChar, self.mygame.mineChar, self.mygame.pathChar, self.mygame.boxChar]
		runSettings = True

		def reset(characterList):
			# print(selIndex)
			# print("rests")
			playerChar = "O"
			mineChar = "#"
			pathChar = "."
			boxChar = "_"
			characterList = [playerChar, mineChar, pathChar, boxChar]
			# print(characterList)
			self.mygame.playerChar = characterList[0]
			self.mygame.mineChar = characterList[1]
			self.mygame.pathChar = characterList[2]
			self.mygame.boxChar	= characterList[3]
			return characterList


		while runSettings:
			select = False

			if self.move_list(menulist) == 0:

				self.print_list(menulist)
				selIndex = self.currentSelection

				# Return
				if selIndex == len(menulist)-1:
					runSettings = False
					return 0

				# Reset to Default
				elif selIndex == len(menulist)-2:
					characterList = reset(characterList)

				# Save Changes
				elif selIndex == len(menulist)-3:

					for eachChar in characterList:
						if characterList.count(eachChar)>1:
							print("\nPlease Enter separate, valid characters!")
							time.sleep(1.3)
							characterList = reset(characterList)
							break
					
					self.mygame.playerChar = characterList[0]
					self.mygame.mineChar = characterList[1]
					self.mygame.pathChar = characterList[2]
					self.mygame.boxChar	= characterList[3]
					self.save_to_disk(characterList)
					print("\n Changes Saved!")
					time.sleep(1)
				else:
					select = True
					print("Please type your chosen symbol.")
				while select == True:
					if msvcrt.kbhit():
						char = self.capture_input()[0]
						menulist[selIndex] = menulist[selIndex][:-1] + str(char)
						print(selIndex)
						characterList[selIndex] = char
						select = False

				for i in range(4):
					# print('yes')
					# time.sleep(0.2)
					# print(menulist)
					# print(characterList)
					menulist[i] = menulist[i][:-1] + characterList[i]

				self.print_list(menulist)


	# Credits function
	def credits(self):
		credits = """CREDITS:\n
		\nAdrien Plisson: Inspiration for restrict function\nPraveen Gollakota: Inspiration for Dispatcher method\nRealPython: Basic Python usage and Syntax\nGeeksForGeeks: Class members and Terminal size usage\n\n[ Press ANY KEY to Return to Main Menu ]
		\n© Copyright Muse_HD 2021 """
		print(credits)
		self.wait()
		return 0
	# Game exit
	def exit(self):
		self.save_highscore()
		sys.exit("Thank you for playing my game!")
		

	# Method for printing list
	def print_list(self, menulist, cls = True):
		listIndex = 0
		# clear = '\033[{0}A'.format(len(menulist)+1)
		width= os.get_terminal_size().columns
		half = width/2

		# Clear screen vs moving cursor
		if cls:
			self.cls()
		else:
			print()
			print('\033[{0}A'.format(len(menulist)+2))

		# Add padding to center menu items
		for listIndex, option in enumerate(menulist):
			blankchars = half - len(option)/2
			chars = ""
			for x in range(int(blankchars)):
				chars += " "
			
			# Highlight selected menu lists
			if listIndex == self.currentSelection:
				print((chars + color.SELECT + color.BLACK + option + color.BASE))
			else:
				print((chars + option))

	# Gets keystrokes (and arrows) and returns a single string
	def capture_input(self):

		key_stroke = msvcrt.getch()
		if ord(key_stroke) == 224:
			key = ord(msvcrt.getch())
			if key == 80:
				key_stroke = b's'
			elif key == 72:
				key_stroke = b'w'
			elif key == 75:
				key_stroke = b'a'
			elif key == 77:
				key_stroke = b'd'
			else:
				pass
		try:
			key_stroke = (str(key_stroke, 'utf-8'))
		except UnicodeDecodeError:
			pass

		self.keylog.append(key_stroke)
		return key_stroke


	# Function that moves the current selection through the menu list
	def move_list(self, menulist, cls = True):
		keylist = {"w":-1, "s":+1}
		scroll = True


		while scroll == True:
			if msvcrt.kbhit():
				key_stroke = self.capture_input()


				if key_stroke == "\r" or key_stroke == " ":
					if cls == True:
						self.cls()
					scroll = False
					return 0

				
				elif key_stroke in keylist:
					direction = (keylist[key_stroke])

				# Copy instance variable to a local var and add the direction 
					currentSelection = self.currentSelection
					currentSelection += direction

					# Conditions to prevent menu list from wrapping around 
					if currentSelection > len(menulist)-1:
						currentSelection -= 1
					elif currentSelection < 0:
						currentSelection += 1

					self.currentSelection = currentSelection

				self.print_list(menulist,cls)




	#   # If Enter or Spacebar is pressed, the currently selected function from the menu list is called using eval
	def main_menu(self):
		mainlist = ["Play","Instructions","Leaderboard","Settings","Credits","Exit"]

		# Contains a list of all menu items with lowercase letters to match the specific functions created for them.
		dispatch = ["self." + menuitem.lower() for menuitem in mainlist]

		if self.move_list(mainlist) == 0:
			if eval(dispatch[self.currentSelection])() == 0:
				self.currentSelection = 0
				self.print_list(mainlist)
				return 0
	

	def update(self):
		self.capture_input()

# Main Control 
menu = UI()
menu.print_list(menu.menulist)


while True:
	if msvcrt.kbhit():
		menu.main_menu()