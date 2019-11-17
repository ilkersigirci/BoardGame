class Cell:
	
	cells = []

	def __init__(self,cellno,description,action="",artifact=""):
		self.cellno = cellno
		self.description = description
		self.action = action
		self.artifact = artifact
		Cell.cells.append(self)
	
