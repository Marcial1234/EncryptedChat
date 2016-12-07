# Client and Server's common variables
max_size = 1000

## Meta Generator code
# max = 13
# oink = []
# for n in xrange(2, max):
# 	oink.append([])
# 	for p in xrange(0, max-1):
# 		r = n**p % max
# 		if r not in oink[n-2]:
# 			oink[n-2].append(r)
# for o in oink:
# 	if len(o) == max-1:
# 		print oink.index(o) + 2

# version 2
# oink = set([])
# numbers = []
# for n in xrange(2, max):
# 	for p in xrange(0, max-1):
# 		r = n**p % max
# 		if r in oink:
# 			break
# 		else:
# 			oink.add(r)
# 	if len(oink) == max-1:
# 		numbers.append(n)
# 	oink = set([])