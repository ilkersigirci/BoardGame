import socket
def Singleton(cls):
	'''generic python decorator to make any class
	singleton.'''
	_instances = {}	  # keep classname vs. instance
	def getinstance():
		'''if cls is not in _instances create it
		and store. return the stored instance'''
		if cls not in _instances:
			_instances[cls] = cls()
		return _instances[cls]
	return getinstance

'''
class Network:
	def __init__(self,port= 2331, host = "127.0.0.1"):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addr = (host, port)
		self.clientCon = None # server tarafindan cagrilinca buralar baglanacak clientler icin gerekli olacak
		self.clientAddr = None # kullanmazsak kaldirabiliriz cunku clientCon uzerinden communicate ediyoruz
        #self.id = self.connect()  bu gerekli mi?
		self.isConnectionEnded = False
	def initCon(self,clientCon):
		self.clientCon = clientCon
		#self.clientSocket.connect(self.addr)
	def initConnectionForClients(self):
		self.serverSocket.bind(self.addr)
		self.serverSocket.listen(1)
	def acceptConnectionFromClient(self):
		self.clientCon,self.clientAddr = self.serverSocket.accept()
		self.clientSocket.connect(self.addr)
		print(self.clientAddr, " connected") 
		return self.clientCon
	
	def receiveData(self):
		#self.clientSocket.connect(self.addr) # bunu her defasinda cagirmak sorun olursa ayri connect fonksiyounu calistir
		return self.clientSocket.recv(2048).decode()
	
	def updateClient(self,data): 
		try:
			self.serverSocket.send(str.encode(data))
		except socket.error as e:
			return str(e)
	def closeConnection(self):
		try:
			self.serverSocket.close()
		except socket.error as e:
			pass
		try:
			self.clientSocket.close()
		except socket.error as e:
			pass

		self.isConnectionEnded = True
'''


""" @Singleton
class OSubject:
	def __init__(self):
		self.connections = []
	def register(self,connection): 
		self.connections.append(connection)
		return self.connections.index(connection)
		#burada indexini donebiliriz ulasim rahat olsun diye
	def unregister(self,id):
		try:
			self.connections[id].close()
		except:
			pass
	def notifyOne(self, id, data): # boku no hero esintisi eklenebilir :)
		self.connections[id].send((data))
	def notifyAll(self,data):
		for connection in self.connections:
			try:
				connection.send((data))
			except:
				pass
 """


@Singleton
class OSubject:
	def __init__(self):
		self.connections = []
		#self.id = -1
	def register(self,connection): 
		self.connections.append(connection)
		#self.id += 1
		return self.connections.index(connection)
		return self.id
	def unregister(self,id):
		try:
			self.connections[id].close()
		except:
			pass
	def notifyOne(self, id, data): # boku no hero esintisi eklenebilir :)
		self.connections[id].send((data))
	def notifyAll(self,data):
		for connection in self.connections:
			try:
				connection.send((data))
			except:
				pass


