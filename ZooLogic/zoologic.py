from copy import deepcopy
class Piece:
	def __init__(self, name, nature, avoid=[]):
		self.name = name
		self.nature = nature
		self.avoid = avoid[:]
	def __str__(self):
		if self.nature == 'Extra':
			return "%s".lower() % str(self.name)	
		return "%s".lower() % self.name
	def addAvoid(self, piece):
		if not self.avoid.count(piece):
			self.avoid.append(piece)
			piece.addAvoid(self)
	def __repr__(self):
		if self.nature == 'Extra':
			return "<Extra: %s>" % str(self.name)	
		return "<Piece: %s>" % self.name

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
			#print "%d\nblacklist: %r\nwhitelist: %r" % (self.key, blacklist, whitelist)
			return whitelist
	def __str__(self):
		if not self.value:
			return "{number: %d, label: empty}" % self.key
		else:
			return "{number: %d, label: %s}".lower() % (self.key,str(self.value))
	def addAdj(self, adj):
		if not self.adj.count(adj):
			self.adj.append(adj)
			adj.adj.append(self)
	def __repr__(self):
		if not self.value:
			return "<Row %d: Empty>" % self.key
		else:
			return "<Row %d: %s>" % (self.key,str(self.value))

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def printJsonTable(table, hand, pos=-1):
	response = {}
	for row in table:
		response[row.key] = row.toDictionary()
		if not row.isFree():
			if (table.index(row) == pos):
				response[row.key]['actual'] = True
		else:
			response[row.key] = row.toDictionary()
			response[row.key]['possibilities'] = [choice[0].name for choice in row.getPossible(hand)]
	print json.dumps(response)

def printTable(table, hand, pos=-1):
	c=0
	for row in table:
		if not row.isFree():
			if table.index(row) == pos:
				print (bcolors.OKBLUE+"%d: %s"+bcolors.ENDC) % (c,row)
			else:	
				print "%d: %s" % (c,row)
		else:
			print (bcolors.OKGREEN+"%d: %s"+bcolors.ENDC+"\t%r") % (c,row,[choice[0].name for choice in row.getPossible(hand)])
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
	print ""
	freerows = getFreeRows(table)
	if len(freerows) == 0:
		return (table,hand)
	row_pos = [[row,row.getPossible(hand)] for row in freerows]
	if len([True for row, pos in row_pos if not len(pos)]):
		return False
	row_pos.sort(key=(lambda x:len(x[1])))
	row_pos.reverse()
	row,pos = row_pos.pop()
	for choice in pos:
		table_ = deepcopy(table)
		hand_ = deepcopy(hand)
		piece = takeFromHand(hand_, choice[0])
		if piece:
			table_[row.key].value = piece
			print level, row.key, piece
			printTable(table_,hand_,row.key)
			solution = solve(table_,hand_,level+1,row_pos=deepcopy(row_pos))
			if solution:
				return solution
			else:
				print "failed"
				printTable(table,hand,row.key)
				print ""
	final.append([table,hand])
	return False
