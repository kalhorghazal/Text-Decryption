STOP = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', \
'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', \
 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', \
 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', \
 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', \
 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', \
 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', \
 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', \
 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', \
 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', \
 'how', 'further', 'was', 'here', 'than'}

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

TRAINING_DIR = "global_text.txt"
POPULATION_SIZE = 60
CHROMOSOME_SIZE = 26
TOURNAMENT_SIZE = 18
CROSSOVER_PROBABILITY = 0.65
MUTATION_PROBABILITY = 0.1
NONE_INT = -1

import random

class Decoder:
	def __init__(self, encoded_text):
		self.encoded_text = encoded_text
		self.decoded_text = ""
		self.population = []
		self.mating_pool = []
		self.fitness = [0] * POPULATION_SIZE
		training_text = open(TRAINING_DIR).read()
		self.dictionary = process_text(training_text)
		self.finished = False


	def initiate_population(self):
		for i in range(POPULATION_SIZE):
			key = random.sample(ALPHABET, len(ALPHABET))
			while key in self.population:
				random.shuffle(key)
			self.population.append(key[:])


	def fill_mating_pool(self):
		self.mating_pool = []
		while  len(self.mating_pool) != POPULATION_SIZE:
			index = self.tournament_select()
			self.mating_pool.append(self.population[index][:])


	def tournament_select(self):
		best_index = NONE_INT
		for i in range(TOURNAMENT_SIZE):
			rand_index = random.randint(0, POPULATION_SIZE-1)
			if best_index == NONE_INT or self.fitness[best_index] < self.fitness[rand_index]:
				best_index = rand_index
		return best_index


	def evaluate_fitness(self):
		for i in range(POPULATION_SIZE):
			table = dict(zip(self.population[i], ALPHABET))
			translated_text = translate_text(self.encoded_text, table)
			processed_text = process_text(translated_text)

			state = True
			self.fitness[i] = 0
			for word in processed_text:
				if word in self.dictionary:	
					self.fitness[i] += len(word)
				else:
					state = False

			if state:
				self.decoded_text = translated_text
				self.finished = True
		#print(sorted(self.fitness, reverse=True)[0])


	def apply_mutation(self, chromosome, point1, point2):
		key = chromosome[:]
		key[point1] = chromosome[point2]
		key[point2] = chromosome[point1]
		return key


	def mutation(self): 
		for i in range(POPULATION_SIZE):
			for j in range(CHROMOSOME_SIZE):
				if random.random() < MUTATION_PROBABILITY:
					point1 = random.randint(0, CHROMOSOME_SIZE-1)
					point2 = random.randint(0, CHROMOSOME_SIZE-1)
					while point1 == point2:
						point2 = random.randint(0, CHROMOSOME_SIZE-1)
					self.mating_pool[i] = self.apply_mutation(self.mating_pool[i], point1, point2)


	def apply_crossover(self, chromosome1, chromosome2, point):
		child = [None] * CHROMOSOME_SIZE
		for i in range(point):
			child[i] = chromosome1[i]

		pos = point
		for i in range(CHROMOSOME_SIZE):
			if pos > (CHROMOSOME_SIZE-1):
				break

			if chromosome2[i] not in child:
				child[pos] = chromosome2[i]
				pos += 1
		return child


	def crossover(self):
		mating_pool = []
		index = set()
		while len(mating_pool) != POPULATION_SIZE:
			point = random.randint(1, CHROMOSOME_SIZE-2)

			index1 = random.randint(0, POPULATION_SIZE-1)
			while index1 in index:
				index1 = random.randint(0, POPULATION_SIZE-1)

			index.add(index1)

			parent1 = self.mating_pool[index1]

			index2 = random.randint(0, POPULATION_SIZE-1)
			while index2 == index1:
				index2 = random.randint(0, POPULATION_SIZE-1)

			while index2 in index:
				index2 = random.randint(0, POPULATION_SIZE-1)

			index.add(index2)

			parent2 = self.mating_pool[index2]
		
			if random.random() < CROSSOVER_PROBABILITY:
				child1 = self.apply_crossover(parent1, parent2, point)
				child2 = self.apply_crossover(parent2, parent1, point)
				mating_pool.append(child1)
				mating_pool.append(child2)
			else:
				mating_pool.append(parent1)
				mating_pool.append(parent2)


		self.mating_pool = mating_pool


	def decode(self):
		self.initiate_population()
		while self.finished != True:

			self.evaluate_fitness()
			self.fill_mating_pool()
			self.crossover()
			self.mutation()
			self.population = self.mating_pool[:]
			global MUTATION_PROBABILITY
			if MUTATION_PROBABILITY > 0.02:
				MUTATION_PROBABILITY -= 0.0002

		return self.decoded_text


def process_text(text):
	processed_text = "".join([c if (c.isalpha()) else ' ' for c in text])
	processed_text = processed_text.split()
	processed_text = [word.lower() for word in processed_text]
	processed_text = [word for word in processed_text if word not in STOP]
	processed_text = [word for word in processed_text if len(word) > 1]
	processed_text = set(processed_text)
	return processed_text


def translate_text(text, dictionary):
	translated_text = ""
	for i in range(len(text)):
		if text[i].isalpha():
			if text[i].isupper():
				translated_text += dictionary[text[i].lower()].upper()
			else:
				translated_text += dictionary[text[i]]
		else:
			translated_text += text[i]
	return translated_text
