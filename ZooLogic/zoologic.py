from copy import deepcopy
class Piece:
	def __init__(self, name, nature, avoid=[]):
		self.name = name
		self.nature = nature
		self.avoid = avoid[:]
	def __str__(self):
		if self.nature == 'Extra':
			return "<Extra: %s>" % str(self.name)	
		return "<Piece: %s>" % self.name
	def addAvoid(self, piece):
		if not self.avoid.count(piece):
			self.avoid.append(piece)
			piece.addAvoid(self)
	def __repr__(self):
		return str(self)

class Row:
	def __init__(self, key, value = False, adj = [], locked = False):
		self.key = key
		self.value = value
		self.adj = []
		self.locked = locked
	def isFree(self):
		if not self.value or self.value.nature == 'Extra':
			return True
		return False
	def getAvoidList(self):
		if self.isFree():
			return []
		else:
			return self.value.avoid
	def getPossible(self, hand):
		hand = [kind for kind in hand if len(kind)]
		if self.locked:
			return []
		else:
			blacklist = []
			whitelist = []
			for row in self.adj:
				blacklist.extend(row.getAvoidList())
			if self.value and self.value.nature == 'Extra':
				blacklist.extend([piece[1] for piece in pieces.items() if piece[1].nature==self.value.avoid])
			blacklist = [row.name for row in blacklist]
			for choices in hand:
				if not blacklist.count(choices[0].name):
					whitelist.append(choices)
			return whitelist
	def __str__(self):
		if not self.value:
			return "<Row %d: Empty>" % self.key
		else:
			return "<Row %d: %s>" % (self.key,str(self.value))
	def addAdj(self, adj):
		if not self.adj.count(adj):
			self.adj.append(adj)
			adj.adj.append(self)
	def __repr__(self):
		return str(self)

pieces = {}
#Animals
pieces['cat'] = Piece("Cat",nature='Animal')
pieces['angry_dog'] = Piece("Angry Dog",nature='Animal')
pieces['calm_dog'] = Piece("Calm Dog",nature='Animal')
pieces['mouse'] = Piece("Mouse",nature='Animal')

#Foods
pieces['cheese'] = Piece("Cheese",nature='Food')
pieces['fish'] = Piece("Fish",nature='Food')
pieces['bone'] = Piece("Bone",nature='Food')

#Extras
pieces['ants'] = Piece("Ants",nature='Extra',avoid='Food')
pieces['bull'] = Piece("Raging Bull",nature='Extra',avoid='Animal')

#Avoid its foods
pieces['cat'].addAvoid(pieces['fish'])
pieces['mouse'].addAvoid(pieces['cheese'])
pieces['angry_dog'].addAvoid(pieces['bone'])
pieces['calm_dog'].addAvoid(pieces['bone'])

#Avoids its preys and hunters
pieces['cat'].addAvoid(pieces['mouse'])
pieces['cat'].addAvoid(pieces['calm_dog'])
pieces['cat'].addAvoid(pieces['angry_dog'])

#Avoids its own similars
pieces['angry_dog'].addAvoid(pieces['calm_dog'])
pieces['angry_dog'].addAvoid(pieces['angry_dog'])

def getFreeRows(table):
	return [row for row in table if row.isFree()]

def printTable(table,hand):
	c=0
	for row in table:
		if not row.isFree():
			print "%d: %s" % (c,row)
		else:
			print "%d: %s\t%r" % (c,row,[choice[0].name for choice in row.getPossible(hand)])
		c+=1

def takeFromHand(hand,piece):
	for choices in hand:
		if len(choices) and choices[0].name == piece.name:
			return choices.pop()
	return False

steps = []
final = []
def solve(table, hand, level=0, row_pos=False):
	steps.append([table,hand])
	freerows = getFreeRows(table)
	if len(freerows) == 0:
		return (table,hand)
	if not row_pos:
		row_pos = [[row,row.getPossible(hand)] for row in freerows]
	if len([True for row, pos in row_pos if not len(pos)]):
		return False
	row_pos.sort(key=(lambda x:len(x[1])))
	row_pos.reverse()
	row,pos = row_pos.pop()
	for choice in pos:
		table_ = deepcopy(table)
		hand_ = deepcopy(hand)
		table_[row.key].value = takeFromHand(hand_, choice[0])
		solution = solve(table_,hand_,level+1,row_pos=deepcopy(row_pos))
		if solution:
			return solution
	final.append([table,hand])
	return False
