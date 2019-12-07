class Artifact:

	def __init__(self,name,owned,price,action=""):
		self.name = name
		self.owned = owned
		self.price = price
		self.action = action



class Cell:
	
	#cells = []

	def __init__(self,cellno,description,action="",artifact=""):
		self.cellno = cellno
		self.description = description
		self.action = action
		self.artifact = artifact
		#Cell.cells.append(self)
