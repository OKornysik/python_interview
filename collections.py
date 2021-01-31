#chunks = [(0, 1)] * 2
#print(chunks)
#chunks[0][0] = 42
#print(chunks)

x = 0, 1
y = 5, 8
z = x + y
print(z, 'z = ', id(z), 'x = ', id(x), 'y = ', id(y))

seen = set()
for i in range(1, 4):
    seen.add(i) 
seen.update([8], [9], [(1, 2)])
print(seen)

d = {'k': 1, 'l': 2}
c = {x for x in d.values()}
print(d, c, type(d), type(c))
