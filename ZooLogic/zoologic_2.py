from zoologic import *

table = []
for x in range(10):
	table.append(Row(x))

hand = [
			[pieces['calm_dog'],pieces['calm_dog'],pieces['calm_dog']],
			[pieces['cat']],
			[pieces['cheese'],pieces['cheese']],
			[pieces['bone'],pieces['bone']]
		]
connections = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [0, 2], [2, 4], [4, 6], [6, 8], [1, 3], [3, 5], [5, 7], [7, 9]]
for con in connections:
	table[con[0]].addAdj(table[con[1]])

table[6].value = pieces['mouse']
table[2].value = pieces['mouse']
table[9].value = pieces['ants']

printTable(table,hand)

table, hand = solve(table, hand)
print "N# of Steps: %d" % len(steps)
print "N# of Dead Ends: %d" % len(final)
