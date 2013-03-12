from copy import deepcopy

class Rooms:
	def __init__(self,rooms=[1,1],current_room=0,final_state=[0,0]):
		self.rooms=rooms
		self.current_room=current_room
		self.final_state=final_state
	def clean_room(self):
		self.rooms[self.current_room] = 0
		return "Cleaning room: %r" % self.current_room
	def move_to_room(self,room):
		self.current_room = room
		return "Going to room: %r" % self.current_room
	def get_actions(self):
		actions = [(lambda: self.move_to_room(room)) for room in self.rooms if not room == self.current_room]
		if self.rooms[self.current_room]!=0:
			actions.append(self.clean_room)
		return actions
	def is_final_state(self):
		if self.rooms == self.final_state:
			return True
		return False
	def __unicode__(self):
		return u"[%r - %r]" % (self.rooms,self.current_room)
	
class Vacuum:
	def __init__(self,rooms=Rooms()):
		self.rooms = rooms
		self.states = []
	def go_one(self,tree):
		if self.rooms.is_final_state():
			tree.append("Finished!")
			return tree
		elif tree.count(unicode(self.rooms)) != 0:
			tree.append("Failed!")
			return False
		for action in self.rooms.get_actions():
			tree.append(action())
			this_state = unicode(deepcopy(self.rooms))
			tree.append(this_state)
			state = self.go_one(tree)
			if state:
				return state
		return tree
	def run(self):
		print self.go_one([])

vacuum = Vacuum()
vacuum.run()

