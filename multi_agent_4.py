#!/usr/bin/env python
# coding: utf-8

# # A*

# In[1]:


from queue import PriorityQueue
import numpy as np
from enum import Enum


# In[2]:


class Action(Enum):
    """
    An action is represented by a 3 element tuple.
    
    The first 2 values are the delta of the action relative
    to the current grid position. The third and final value
    is the cost of performing the action.
    """
    LEFT = (0, -1, 1)
    RIGHT = (0, 1, 1)
    UP = (-1, 0, 1)
    DOWN = (1, 0, 1)
    HOLD = (0, 0, 0)
    
    def __str__(self):
        if self == self.LEFT:
            return '<'
        elif self == self.RIGHT:
            return '>'
        elif self == self.UP:
            return '^'
        elif self == self.DOWN:
            return 'v'
    
    @property
    def cost(self):
        return self.value[2]
    
    @property
    def delta(self):
        return (self.value[0], self.value[1])
            
    
def valid_actions(grid, current_node):
    """
    Returns a list of valid actions given a grid and current node.
    """
    valid = [Action.UP, Action.LEFT, Action.RIGHT, Action.DOWN]
    n, m = grid.shape[0] - 1, grid.shape[1] - 1
    x, y = current_node
    
    # check if the node is off the grid or
    # it's an obstacle
    
    if x - 1 < 0 or grid[x-1, y] == 1:
        valid.remove(Action.UP)
    if x + 1 > n or grid[x+1, y] == 1:
        valid.remove(Action.DOWN)
    if y - 1 < 0 or grid[x, y-1] == 1:
        valid.remove(Action.LEFT)
    if y + 1 > m or grid[x, y+1] == 1:
        valid.remove(Action.RIGHT)
        
    return valid

def visualize_path(grid, path, start):
    sgrid = np.zeros(np.shape(grid), dtype=np.str)
    sgrid[:] = ' '
    sgrid[grid[:] == 1] = 'O'
    
    pos = start
    
    for a in path:
        # a has enumerated variable
        da = a.value
        sgrid[pos[0], pos[1]] = str(a)
        pos = (pos[0] + da[0], pos[1] + da[1])
    sgrid[pos[0], pos[1]] = 'G'
    sgrid[start[0], start[1]] = 'S'  
    return sgrid

def update_path(tag, path2):
    path_new = []
    for i in range(len(path2)):
        if i is tag:
            path_new.append(Action.HOLD)
        path_new.append(path2[i])

    return path_new


def check_collision(start, path):
    start1 = start[0]
    start2 = start[1]
    path1 = path[0]
    path2 = path[1]
    pos2 = start2
    pos1 = start1
    path_new = path2

    # print("hello  = ", path_new)
    count = 0
    tag = 0
    print("path 1", len(path[0]) )
    print("path 2", len(path[1]) )
    n = np.argmin([len(path[0]), len(path[1])])
    print("min length", n)
    # for a,b in zip(path1, path2):
    for i in range(len(path[n])):
        a = path[0][i]
        b = path_new[i]
        bot1 = a.delta
        bot2 = b.delta
        print("bot1 = ",bot1)
        print("pos1 = ", pos1)
        # print(pos1, pos2)

        pos1 = (pos1[0] + bot1[0], pos1[1]+ bot1[1])
        pos2 = (pos2[0] + bot2[0], pos2[1]+ bot2[1])
        # print("pos = ", pos2)
        if pos2 == pos1:
            tag = count
            print("yess")
            path_new = update_path(tag, path_new)

        count+=1
        path[1] = path_new
    
    
    
    return (path1, path_new)

# ## Heuristics
# The heuristic function determines the $h()$ value for each cell based on the goal cell and the method chosen to determine it. The heuristic value can be the Euclidean distance between these cells $h= \left((x_i-x_{goal})^2+(y_i-y_{goal})^2\right)^{1/2}$ or the "Manhattan distance", which is the minimum number of moves required to reach the goal from the assigned cell $h = ||x_i-x_{goal}|| + ||y_i-y_{goal}||$. For this exercise you could use either, or something else which is *admissible* and *consistent*.
# 
# The input variables include
# * **```position```** the coordinates of the cell for which you would like to determine the heuristic value.
# * **```goal_position```** the coordinates of the goal cell

# In[4]:


# TODO: implement a heuristic function. This may be one of the
# functions described above or feel free to think of something
# else.
def heuristic(position, goal_position):
    h = 0
    h = (position[0] - goal_position[0])**2 + abs(position[1] - goal_position[1])**2
    h = h*20
    #h = abs(position[0] - goal_position[0]) + abs(position[1] - goal_position[1])
    return h


# ## A* search
# 
# A* search is an extension of the cost search you implemented. A heuristic function is used in addition to the cost penalty. Thus if the setup is:
# 
# * $c$ is the current cost
# * $g$ is the cost function
# * $h$ is the heuristic function
# 
# Then the new cost is $c_{new} = c + g() + h()$.
# 
# The difference between $g$ and $h$ is that $g$ models the cost of performing actions, irrespective of the environment, while $h$ models the cost based on the environment, i.e., the distance to the goal.

# You know what comes next, turn the `TODOs` into `DONEs` :)

# In[5]:

def print_pos(start, path):
    pos = start
    steps = []
    for i in range(len(path)):
        a = path[i]
        bot = a.delta
        pos = (pos[0] + bot[0], pos[1]+ bot[1])
        steps.append(pos)
    print(steps)

def a_star(grid, h, start, goal):

    path = []
    path_cost = 0
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set(start)

    branch = {}
    found = False
    
    while not queue.empty():

        # gives the item which has min cost = (branch + heuristics)
        item = queue.get()

        current_node = item[1]
        if current_node == start:
            current_cost = 0.0
        else:
            ## takes only branch cost and not heuristics              
            current_cost = branch[current_node][0]
            
        if current_node == goal:        
            print('Found a path.')
            found = True
            break
        else:
            for action in valid_actions(grid, current_node):
                # get the tuple representation
                da = action.delta
                next_node = (current_node[0] + da[0], current_node[1] + da[1])
#                 # TODO: calculate branch cost (action.cost + g)
#                 g = current_cost + action.cost
#                 # TODO: calculate queue cost (action.cost + g + h)
#                 f = g + h(next_node, goal)
#                 branch_cost = g
#                 queue_cost = f
                branch_cost = current_cost + action.cost
                queue_cost = branch_cost + h(next_node, goal)
                
                if next_node not in visited:                
                    visited.add(next_node)               
                    branch[next_node] = (branch_cost, current_node, action)
                    queue.put((queue_cost, next_node))    
                    
    if found:
        # retrace steps
        n = goal
        path_cost = branch[n][0]
        while branch[n][1] != start:
            # path stores only the action
            path.append(branch[n][2])
            n = branch[n][1]
        path.append(branch[n][2])
    else:
        print('**********************')
        print('Failed to find a path!')
        print('**********************')
        
    return path[::-1], path_cost
    #h = abs(position[0] - global_position[0]) + abs(position[1] - position[1])


# In[6]:


start = [(4,0), (2,0)]
goal = [(2,5), (3, 5)]
path = []
grid = np.array([
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
])


# In[7]:


path1, cost = a_star(grid, heuristic, start[0], goal[0])
path2, cost = a_star(grid, heuristic, start[1], goal[1])
# print(path, cost)
path.append(path1)
path.append(path2)

# In[8]:


# S -> start, G -> goal, O -> obstacle
print(visualize_path(grid, path[1], start[1]))

path_new_1, path_new_2 = check_collision(start, path)


print_pos(start[1], path_new_2)
print_pos(start[1], path2)


# print(path_new_2)
print_pos(start[0], path_new_1)

print_pos(start[0], path1)

# [Solution](/notebooks/A-Star-Solution.ipynb)

# In[ ]:




