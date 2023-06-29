class Node:
	def __init__(self,name,parent):
		self.name = name
		self.parent = parent
		self.value = [0,0,0]
		self.path = []
		self.trail = []
