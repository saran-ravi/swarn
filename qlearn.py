import numpy as np
import time
location_to_state = {'l1':0, 'l2':1, 'l3':2, 'l4':3, 'l5':4, 'l6':5, 'l7':6, 'l8':7, 'l9':8 }
actions = [0,1,2,3,4,5,6,7,8,9]
rewards = np.array([[0,1,0,0,0,0,0,0,0],
					[1,0,1,0,0,0,0,0,0],
					[0,1,0,0,0,1,0,0,0],
					[0,0,0,0,0,0,1,0,0],
					[0,1,0,0,0,0,0,1,0],
					[0,0,1,0,0,0,0,0,0],
					[0,0,0,1,0,0,0,1,0],
					[0,0,0,0,1,0,1,0,1],
					[0,0,0,0,0,0,0,1,0]])
state_to_location = dict((state, location) for location, state in location_to_state.items())

# print(state_to_location)
gamma = 0.5  # discount
alpha = 0.9   # learning rate

q = np.array(np.zeros([9,9]))

# reward_copy = np.copy(rewards)

# Input to end location

# end_location = 'l1'

# end_state = location_to_state[end_location]

# reward_copy[end_state,end_state] = 999

# print(np.argmax(rewards[0]))




def get_optimal_route(start_location, end_location):
	
	reward_copy = np.copy(rewards)
	end_state = location_to_state[end_location]
	reward_copy[end_state,end_state] = 999
	q = np.array(np.zeros([9,9]))

	for i in range(2000):

		# e = input(" ckeck ")
		current_state = np.random.randint(0,9)
		playable_action = []
		# print("current_state = ",current_state) ###check

		for j in range(9):
			if reward_copy[current_state, j] > 0:
				playable_action.append(j)

		next_state = np.random.choice(playable_action)
		# print("next state = ", next_state)  ###check

		print("action of next state = ",np.argmax(q[next_state]))
		print("Q of current_state = ", q[current_state, next_state])

		print(q)


		td = reward_copy[current_state, next_state] + gamma*q[next_state,np.argmax(q[next_state])] - q[current_state, next_state]
		q[current_state, next_state] += alpha*td
		print("temporal difference = ", td)


	route = [start_location]
	print(q)
	next_location = start_location
	c = 0
	while (next_location != end_location):
		c +=1
		start_state = location_to_state[start_location]
		next_state = np.argmax(q[start_state,])
		next_location = state_to_location[next_state]
		start_location = next_location
		route.append(next_location)
	return route

t_beg  =  time.time()
g = get_optimal_route('l1','l3')
t_end = time.time() - t_beg
print(t_end)
print(g)


	





