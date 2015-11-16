import random

class ItpirServer:
	"""ITPIR Server implementation.
	
	ITPIR Server implementation using the 
	Chor-Goldreich-Kushilevitz-Sudan (CGKS) IPPIR Protocol
	"""
	def __init__(self, name, library, l):
		"""Class Constructor.
		
		Initializes the server.
		
		Args:
		    name: Name of the server.
		    library: Objects that need to be delivered to the clients
		    l: lenght l in bits of each of the objects in the library
		"""
		self.name = name
		self.library = library
		self.n = len(library)
		self.l = l

	def answer(self, query):
		"""Sends an answer to a request of the user.
		
		Args:
		    query: query vector received from the user.
		
		Returns:
		    Ciphertext answer for the client.
		"""
		result = 0;
		print("[", self.name, "]", " Got query: " + bin(query))
		for i in range(self.l,0, -1):	# Compute the query . Library result (product over the two element Galois field)
			bit = 0
			for j in range(self.n, 0, -1):
				and1 = query & 2 ** (j-1)
				and2 = self.library[self.n-j] & 2 ** (i-1)
				and1 = 1 if and1 > 0 else 0
				and2 = 1 if and2 > 0 else 0
				bit = bit ^ (and1 & and2)
			result = result << 1
			result = result | bit
		print("[", self.name, "]", " Answer to be sent: " + bin(result))
		return result


class ItpirClient:
	"""Represents a Client for the ITPIT protocol.
	
	Represents a client of the ITPIR protocol, which requests objects
	to the servers without revealing which object he wants.
	
	Args:
	    n: The length of the object library. Each object can be accessed with 
	    	a number going from 1 to n
	    servers: The servers that are part of the ITPIR infrastructure and that have the media objects
	    l: lenght l in bits of each of the objects in the library
	"""
	def __init__(self, n, servers, l):
		self.n = n
		self.servers = servers
		self.l = l
		self.maxRandomQuery = 0
		for x in range(0,self.n):
			self.maxRandomQuery = (self.maxRandomQuery << 1) | 1


	def watch(self, index):
		"""Start point to watch a movie.
		
		Initiates the process of media consumption.
		
		Args:
		    index: Number from 1 to n of the movie that the client wants to watch.
		"""
		print("[CLIENT] I want to watch movie #", index)
		query = self.query(index)							#Get the queries for each server
		answers = []
		for i in range(0, len(query)):
			answer_i = self.servers[i].answer(query[i])		#Get the answer from each server
			answers.append(answer_i)
		self.__printAnswers(answers)
		movie = self.decode(answers)						#Decode the answers from the servers to get the movie 
		print("[CLIENT] Watching movie #", index)
		print("[CLIENT] Watching movie: ", bin(movie))
		return

	def query(self, index):
		"""Creates the queries that are going to be sent to the servers.
		
		Creates the queries that are going to be sent to the servers.
		
		Args:
		    index: Number from 1 to n of the movie that the client wants to watch.
		
		Returns:
		    The query vector to request object 'index'.
		"""
		query = []
		for server in range(0,len(self.servers) - 1):
			qj = random.randint(1, self.maxRandomQuery)
			query.append(qj)
		eb = 2**(self.n-index);
		qk = eb
		for qj in query:
			qk = qk ^ qj
		query.append(qk)
		self.__printQuery(query);
		return query

	def decode(self, answers):
		"""Decodes the answers from the ITPIR Servers.

		Returns:
		    The decoded object.
		"""
		print("[CLIENT] - Decoding...")
		result = 0						#Decodes the answer by XORing all the individual answers
		for answer in answers:
			result = result ^ answer
		return result
		

	def __printQuery(self, query):
		print("[CLIENT] Generated Query Vectors")
		for q in query:
			print(bin(q))
		print("********************************")

	def __printAnswers(self, answers):
		for i in range(0, len(answers)):
			print('[CLIENT] Answer of', self.servers[i].name, ': ', bin(answers[i]))



#########
# EXAMPLE
#########
l = 5

library = []
library.append(30)
library.append(28)
library.append(5)
library.append(23)
library.append(18)
library.append(15)
library.append(19)
library.append(1)
library.append(12)

print("----Library---------------------------------")
for i in range(0, len(library)):
	print("Movie #", (i+1), ": ", bin(library[i]))
print("--------------------------------------------")

server_one = ItpirServer("Server One", library, l)
server_two = ItpirServer("Server Two", library, l)
client = ItpirClient(len(library), [server_one, server_two], l)
client.watch(9)




