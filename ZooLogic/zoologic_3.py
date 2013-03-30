from zoologic import *
import json

table = []
for x in range(8):
	table.append(Row(x))

hand =	[
			[pieces['calm_dog']],
			[pieces['mouse'],pieces['mouse']],
			[pieces['cheese']],
			[pieces['bone'],pieces['bone']]
		]
connections = [[0,1],[1,3],[0,2],[2,4],[3,4],[2,5],[4,7],[4,5],[6,7],[3,6],[5,7],[4,6]]
for con in connections:
	table[con[0]].addAdj(table[con[1]])

table[0].value = pieces['fish']
table[2].value = pieces['bull']
table[6].value = pieces['fish']
table[7].value = pieces['bull']
	
printTable(table,hand)

table, hand = solve(table, hand)
print "N# of Steps: %d" % len(steps)
print "N# of Dead Ends: %d" % len(final)
