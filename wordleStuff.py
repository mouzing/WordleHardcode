import random
import string

wordleList = []

with open('wordleWord.txt') as file:
    wordleList = file.readlines()
    wordleList = wordleList[:-1]

for i, word in enumerate(wordleList):
	wordleList[i] = word[:-1]

#print(wordleList)

WordOfTheRound = random.choice(wordleList)
print(WordOfTheRound)

rounds = 6

class gameContainer():
	def __init__(self):
		self.currentRound = 1
		self.latestGuess = ''
		self.guesses = []
		self.notGreyLetters = list(string.ascii_lowercase)
		self.greenLetters = [None] * 5 
		self.orangeLetters = []
		self.indexColorInfo = [None] * 5 # green = look in self.greenLetters. Orange = list of tuples (orange, [list of letters for a position]), grey = whocares


#  t = [ [0]*3 for i in range(3)]

	def generateGuess(self):
		if (self.currentRound == 1):
			guess = random.choice(wordleList)
			self.latestGuess = guess
			self.guesses.append(guess)
		else:
			self.constructGuess()

	def constructGuess(self):
		limit = 0
		while(limit < 10):
			workingGuess = self.greenLetters.copy()
			orangesToUse = self.orangeLetters.copy()
			print(f"oranges to use: {orangesToUse}")
			# use orange letters
			if len(orangesToUse) > 0:
				print("here")
				for i, letter in enumerate(workingGuess):
					if letter is None and len(orangesToUse) != 0:
						if (self.indexColorInfo[i] != None):
							availableLetters = list(set(orangesToUse) - set(self.indexColorInfo[i][1])) 
							workingGuess[i] = random.choice(availableLetters)
							orangesToUse.remove(workingGuess[i])

			# assign the remaining letters
			for i, letter in enumerate(workingGuess):
				if letter is None:
					workingGuess[i] = random.choice(self.notGreyLetters)

			#Local use case: check if it is in the text document
			workingGuessStr = ''.join(workingGuess)
			if self.checkDocument(workingGuessStr):
				self.latestGuess = workingGuessStr
				self.guesses.append(self.latestGuess)
				print(limit)
				break
			
			limit += 1
			if (limit >= 10000):
				print("what the fuck")
				self.latestGuess = workingGuessStr
				self.guesses.append(self.latestGuess)


	def updateOrange(self, i, letter):
		if self.indexColorInfo[i] != 'green':
			if self.indexColorInfo[i] != 'orange':
				self.indexColorInfo[i] = ('orange', [letter])
			else:
				self.indexColorInfo[i][1].append(letter)



	def extractCharacters(self):
		localWOTR = list(WordOfTheRound)
		# check green
		for i, letter in enumerate(self.latestGuess):
			if (letter == localWOTR[i]): 
				self.greenLetters[i] = letter
				self.indexColorInfo[i] = 'green'
				localWOTR[i] = '$'

		# check orange
		seenLetters = []
		for i, letter in enumerate(self.latestGuess):
			if letter in localWOTR:
				localWOTR[localWOTR.index(letter)] = '$'
				if (letter in self.orangeLetters and letter not in seenLetters):
					seenLetters.append(letter)
				elif (letter in self.orangeLetters and letter in seenLetters):
					self.orangeLetters.append(letter)
				else:
					self.orangeLetters.append(letter)

				self.updateOrange(i, letter)

		#remove grey letters from possible choices
		for letter in localWOTR:
			if letter != '$':
				if letter in self.notGreyLetters: self.notGreyLetters.remove(letter)
				


	def checkDocument(self, workingGuessStr):
		if (workingGuessStr in wordleList):
			return True

		return False


gameContainer = gameContainer()
while(gameContainer.currentRound < rounds + 1):

	print(f"current round: {gameContainer.currentRound}")
	gameContainer.generateGuess()
	if (gameContainer.latestGuess == WordOfTheRound):
		print('Winner!')

	gameContainer.extractCharacters()

	gameContainer.currentRound += 1
	print()


print(gameContainer.guesses) # not appending guesse for reason. also not really using the ornage ltters list -> possibly related.
print(gameContainer.greenLetters)
print(gameContainer.orangeLetters)
print(gameContainer.notGreyLetters)
print(gameContainer.indexColorInfo)


