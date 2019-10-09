import numpy as np
# import matplotlib.py as mp
import math

g = 0.1
l = 0.2

count = 10

row = 10
column = 10

grid = np.zeros((row, column))
# print(grid)
dest = [1,3]
# dest_x, dest_y = input().split()
# print(type(dest_x))
# print(dest_y)

bot_a = [0,0]
bot_b = [1,0]
bot_c = [4,2]

a_loc = [bot_a[0] + 1, bot_a[1]]
b_loc = [bot_b[0] + 1, bot_b[1]]
c_loc = [bot_c[0] + 1, bot_c[1]]

a_path = []
b_path = []
c_path = []

def distance(coor, dest):
	# print(coor,dest)

	g = (coor[0] - dest[0])**2 + (coor[1] - dest[1])**2
	d = int(math.sqrt(g))
	return d

def glob(a,b,c):
	x = [[distance(a,dest),a],[distance(b,dest), b],[distance(c,dest),c]]
	y = min(x)
	return y[1]
def next(bot, glo, loc):
	x = int(bot[0]+g*(glo[0]- bot[0]) + l*(loc[0] - bot[0])) + 1
	y = int(bot[1]+g*(glo[1]- bot[1]) + l*(loc[1] - bot[1])) + 1
	if x > row -1:
		x = row -1
	if y > column -1:
		y = column -1
	next_step = [x,y]
	return next_step
def update_local(bot, loc, dest):
	if distance(bot, dest) > distance(loc, dest):
		return loc
	else:
		return bot

while(count>0) :
	
# while((bot_c!=dest) and (bot_b !=dest) and (bot_c !=dest)):

	###global
	g_des = glob(a_loc,b_loc,c_loc)
	print("global", g_des)
	# input()
	###storing location
	a_path.append(bot_a)
	b_path.append(bot_b)
	c_path.append(bot_c)
	###finding next step
	a_next = next(bot_a, g_des, a_loc )
	b_next = next(bot_b, g_des, b_loc )
	c_next = next(bot_c, g_des, c_loc )
	print(" current = ",bot_a,bot_b,bot_c)
	print("next = ",a_next, b_next, c_next)
	###mov next
	bot_a = a_next
	bot_b = b_next
	bot_c = c_next
	## udating new local decision
	a_loc = update_local(bot_a, a_loc, dest)
	b_loc = update_local(bot_b, b_loc, dest)
	c_loc = update_local(bot_c, c_loc, dest)

	print("update_local = ",a_loc, b_loc,c_loc)

	count = count -1
	input()

print(a_path)
print(b_path)
print(c_path)


