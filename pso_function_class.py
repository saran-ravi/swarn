import numpy as np
# import matplotlib.py as mp
import math

g = 0.9
l = 0.9

pi = 3.14
###number of iterations
count = 500


###space design
row = 100
column = 100
# x_min = -10
# x_max = 10
# y_min = -10
# y_max = 10
x_min = 0.5
x_max = 10
y_min = 0.5
y_max = 10

### frame movement

x_frame = 0
y_frame = 0



grid = np.zeros((row, column))
# print(grid)
dest = [80,70]
first_step = 0

# dest_x, dest_y = input().split()
# print(type(dest_x))
# print(dest_y)

###initial positions
# bot_a = [0,0]
# bot_b = [-2.6,2.8]
# bot_c = [0,2]
# bot_a = [9,3]
# bot_b = [2.5,1.8]
# bot_c = [2,3]
bot_a = [np.random.randint(1,21), np.random.randint(1,21)]
bot_b = [np.random.randint(1,21), np.random.randint(1,21)]
bot_c = [np.random.randint(1,21), np.random.randint(1,21)]
bot_d = [np.random.randint(1,21), np.random.randint(1,21)]
bot_e = [np.random.randint(1,21), np.random.randint(1,21)]

a_loc = [bot_a[0] + first_step, bot_a[1] + first_step]
b_loc = [bot_b[0] - first_step, bot_b[1] - first_step]
c_loc = [bot_c[0] - first_step, bot_c[1] + first_step]
d_loc = [bot_c[0] - first_step, bot_c[1] + first_step]
e_loc = [bot_c[0] - first_step, bot_c[1] + first_step]



a_path = []
b_path = []
c_path = []
e_path = []
d_path = []

def distance(coor, dest):
	# print(coor,dest)
	x,y = coor[0] - x_frame, coor[1] - y_frame

	# g = (coor[0] - dest[0])**2 + (coor[1] - dest[1])**2
	# d = int(math.sqrt(g))
	# d = (x**2 + y - 11)**2 + (x + y**2 -7)**2
	d = math.sin(3*pi*x)**2 + ((x-1)**2)*(x+math.sin(3*pi*y)**2) + ((y-1)**2)*(1+math.sin(2*pi*y)**2)
	# print("d = ",d)
	return abs(d)

def glob(a,b,c,d,e):
	x = [[distance(a,dest),a],[distance(b,dest), b],[distance(c,dest),c], [distance(d,dest),d], [distance(e,dest),e] ]
	y = min(x)
	return y[1]
def next(bot, glo, loc):
	###int on x,y was removed
	x = (bot[0]+g*np.random.uniform(0,1)*(glo[0]- bot[0]) + l*np.random.uniform(0,1)*(loc[0] - bot[0])) + np.random.uniform(-0.5,0.5)
	y = (bot[1]+g*np.random.uniform(0,1)*(glo[1]- bot[1]) + l*np.random.uniform(0,1)*(loc[1] - bot[1])) + np.random.uniform(-0.5,0.5)
	# r = np.random.uniform(0,1)
	# x = (bot[0]+ g*r*(glo[0]- bot[0]) + l*(1-r)*(loc[0] - bot[0])) + np.random.uniform(0,1)/5
	# y = (bot[1]+ g*r*(glo[1]- bot[1]) + l*(1-r)*(loc[1] - bot[1])) + np.random.uniform(0,1)/5
	if x > row -1:
		x = row -1
	if y > column -1:
		y = column -1
	next_step = [x,y]
	# print("next_step = ", next_step)
	return next_step
def update_local(bot, loc, dest):
	if distance(bot, dest) > distance(loc, dest):
		return loc
	else:
		return bot
def limit_space(coor):
	x,y = coor[0], coor[1]
	x = np.clip(x, x_min, x_max)
	y = np.clip(y, y_min, y_max)
	return(x,y)
	

while(count>0) :
	
# while((bot_c!=dest) and (bot_b !=dest) and (bot_c !=dest)):

	###global
	g_des = glob(a_loc,b_loc,c_loc,d_loc,e_loc)
	# print("global", g_des)
	# input()
	###storing location
	a_path.append(bot_a)
	b_path.append(bot_b)
	c_path.append(bot_c)
	d_path.append(bot_d)
	e_path.append(bot_e)


	###finding next step
	a_next = next(bot_a, g_des, a_loc )
	b_next = next(bot_b, g_des, b_loc )
	c_next = next(bot_c, g_des, c_loc )
	d_next = next(bot_d, g_des, d_loc )
	e_next = next(bot_e, g_des, e_loc )

	###limting the space
	a_next = limit_space(a_next)
	b_next = limit_space(b_next)
	c_next = limit_space(c_next)
	d_next = limit_space(d_next)
	e_next = limit_space(e_next)

	# print(" current = ",bot_a,bot_b,bot_c)
	# print("next = ",a_next, b_next, c_next)
	###mov next
	bot_a = a_next
	bot_b = b_next
	bot_c = c_next
	bot_d = d_next
	bot_e = e_next
	## udating new local decision
	a_loc = update_local(bot_a, a_loc, dest)
	b_loc = update_local(bot_b, b_loc, dest)
	c_loc = update_local(bot_c, c_loc, dest)
	d_loc = update_local(bot_d, d_loc, dest)
	e_loc = update_local(bot_e, e_loc, dest)

	# print("update_local = ",a_loc, b_loc,c_loc)
	# print("global_decision = ",g_des)
	# input()
	count = count -1
	# input()

print("global", g_des)
print(a_path[-1])
print(b_path[-1])
print(c_path[-1])
print(d_path[-1])
print(e_path[-1])



