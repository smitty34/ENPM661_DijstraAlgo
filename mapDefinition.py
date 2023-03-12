#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 07:17:58 2023

@author: landis
"""

import cv2
import numpy as np
from queue import PriorityQueue
import time
import matplotlib.pyplot as plt


start_time = time.time()



start_x = int(input("Start position for 'x' : "))
start_y = int(input("Start position for 'y' : "))

start_positions = tuple((start_x, start_y))


goal_x = int(input("Goal position for 'x' : "))
goal_y = int(input("Goal position for 'y' : "))

goal_positions = tuple((goal_x, goal_y))




height = 250
width = 600

map_space = np.zeros((height, width,3))


hexagon_shape = lambda x, y : (x >= 235) and (y-50)-((50-88)/(300-235))*(x-300) >= 0 and (y-88)-((88-50)/(365-300))*(x-365) >= 0 and (365 >= x) and (y-200)-((200-162)/(300-365))*(x-300) <= 0 and (y-162)-((162-200)/(235-300))*(x-235) <= 0
          
rectangle1_shape = lambda x, y: (x >100) and (x < 150) and (y >= 150) and (y >= 0)

rectangle2_shape = lambda x, y: (x >=100) & (x <=150) & (y <=100) & (y <= 200)

triangle_shape = lambda x, y: ( x<= 510) and ( x>=460 ) and ( y>= (100/50)*(x-510)+125 ) and (y <=(-100/50)*(x-460) + 225)

mapBounds = lambda x, y: 0 < (5-x) or 0 > (595-x) or 0 < (5-y) or 0 > (245-y)



for x in range(0,map_space.shape[1]):
    
    for y in range(0,map_space.shape[0]):
        
        if hexagon_shape(x, y):
            
            map_space[y, x] = (220,0,0)
            
            
        elif rectangle1_shape(x, y):
            
            map_space[y, x] = (220,0,0)
            
            
        elif rectangle2_shape(x, y):
            
            map_space[y, x] = (220,0,0)
            
        elif triangle_shape(x, y):
            
            map_space[y, x] = (220,0,0)
            
            

            
        else:
            
            map_space[y, x] = 0
            
            
map_space = cv2.flip(map_space,0)


map_space = cv2.flip(map_space, 0)


animated_map = map_space



def hexagon_present(node):
    
   
    
    x, y = [node[0], node[1]]
    
    
    if hexagon_shape(x, y):
        
        return True
    
    else:
        
        return False
    
    
def rectangle1_present(node):
    
    x, y = [node[0], node[1]]
    
    if rectangle1_shape(x, y):
        
        return True
    
    else:
        
        return False
    
    

def rectangle2_present(node):
    
    x, y = [node[0], node[1]]
    
    if rectangle2_shape(x, y):
        
        return True
    
    else:
        
        return False
    
    
def triangle_present(node):
    
    x, y = [node[0], node[1]]
    
    if triangle_shape(x, y):
        
        return True
    
    else:
        
        return False
    
    
def walls_present(node):
    
    x, y = [node[0], node[1]]
    
    
    if (x <= 0) or ( x >= 600) or (y <=0) or (y >= 250):
        
        return True
    
    else:
        
        return False
    
    
def obstacle_checker(node):
    
    if (walls_present(node) or 
        hexagon_present(node) or
        rectangle1_present(node) or
        rectangle2_present(node) or 
        triangle_present(node)) == True:
        
        return True
    
    
    else:
        
        return False
    
    
##

while obstacle_checker(start_positions):
    
    print("Values are within the obstacle regions, please enter new x/y positions")
    
    
    
def moveLeft(world_map):
    
    cost_left = world_map[0]+1
    
    parent_left = world_map[2]
    
    x = world_map[2][0]-1
    y = world_map[2][1]
    
       
    return x, y, cost_left, parent_left


def moveRight(world_map):
    
    cost_right = world_map[0]+1
    
    parent_right = world_map[2]
    
    x = world_map[2][0]+1
    y = world_map[2][1]
    
    
    return x, y, cost_right, parent_right



def moveUp(world_map):
    
    cost_up = world_map[0]+1
    
    parent_up = world_map[2]
    
    x = world_map[2][0]
    y = world_map[2][1]+1
    
    
    return x, y, cost_up, parent_up


def moveDown(world_map):
    
    cost_down = world_map[0]+1
    
    parent_down = world_map[2]
    
    x = world_map[2][0]
    y = world_map[2][1] - 1
    
    
    return x, y, cost_down, parent_down


def moveLeftUp(world_map):
    
    cost_LU = world_map[0]+1.4
    
    parent_LU = world_map[2]
    
    x = world_map[2][0]-1
    y = world_map[2][1]+1
    
    
    return x, y, cost_LU, parent_LU


def moveLeftDown(world_map):
    
    cost_LD = world_map[0]+1.4
    
    parent_LD = world_map[2]
    
    x = world_map[2][0]-1
    y = world_map[2][1]-1
    
    
    return x, y, cost_LD, parent_LD


def moveRightUp(world_map):
    
    cost_RU = world_map[0]+1.4
    
    parent_RU = world_map[2]
    
    x = world_map[2][0]+1
    y = world_map[2][1]+1
    
    
    return x, y, cost_RU, parent_RU


def moveRightDown(world_map):
    
    cost_RD = world_map[0]+1.4
    
    parent_RD = world_map[2]
    
    x = world_map[2][0]+1
    y = world_map[2][1]-1
    
    
    return x, y, cost_RD, parent_RD


def merge(list1, list2):
     
    merged_list = [(p1, p2) for idx1, p1 in enumerate(list1)
    for idx2, p2 in enumerate(list2) if idx1 == idx2]
    return merged_list



a = []
b = []

visited_nodes = []


putIn_queue = PriorityQueue()
    
    
cost_per_move = 0
parent_node = start_x

hold_node = {}


initial_node = (cost_per_move,(parent_node),(start_positions))

putIn_queue.put(initial_node)






while True:
    
    node_ = putIn_queue.get()
    
    
    

    if node_[2] in hold_node:
        
        continue
    
    a.append(node_[2][0])
    b.append(node_[2][1])
    
    
    # Dictionary to Store values
    hold_node[node_[2]] = (node_[1])
    
    
    animated_map[node_[2][1], node_[2][0]] = 0.5
    
    
        

    
    cv2.imshow("Animation Map", animated_map)
    cv2.waitKey(1)
    
    if node_[2] == goal_positions:
        
        print("Reached Focused Goal")
        print(node_)
        
        print("Time for Dijkstra Algorithm to Complete %s" %(time.time() - start_time), " seconds")
        
        break
    
    else:
        
        
        # Moving Left
        
        x_new, y_new, cost_left, parent_left = moveLeft(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                left_node = (cost_left, parent_left, new_position)
                
                putIn_queue.put(left_node)
                
        
        # Moving Right
        
        x_new, y_new, cost_right, parent_right = moveRight(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                right_node = (cost_right, parent_right, new_position)
                
                putIn_queue.put(right_node)
                
                
        # Moving Up
                
        x_new, y_new, cost_up, parent_up = moveUp(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                left_node = (cost_up, parent_up, new_position)
                
                putIn_queue.put(left_node)
                
                
        # Moving Down        
        
        x_new, y_new, cost_down, parent_down = moveDown(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                down_node = (cost_down, parent_down, new_position)
                
                putIn_queue.put(down_node)
                
                
                
        # Moving Up Left
        
        x_new, y_new, cost_UL, parent_UL = moveLeftUp(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                UL_node = (cost_UL, parent_UL, new_position)
                
                putIn_queue.put(UL_node)
                
                
                
        # Moving Down Left
                
        x_new, y_new, cost_DL, parent_DL = moveLeftDown(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                DL_node = (cost_DL, parent_DL, new_position)
                
                putIn_queue.put(DL_node)
                
                
                
        # Moving Up Right
                
        x_new, y_new, cost_UR, parent_UR = moveRightUp(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                UR_node = (cost_UR, parent_UR, new_position)
                
                putIn_queue.put(UR_node)
                
                
                
        # Moving Down Right
        
        
        x_new, y_new, cost_DR, parent_DR = moveRightDown(node_)
        
        new_position = (x_new,y_new)
        
        if obstacle_checker(new_position) == False:
            
            if new_position not in hold_node:
                DR_node = (cost_DR, parent_DR, new_position)
                
                putIn_queue.put(DR_node)
                
g = []
h = []

path_to_home = []

final = goal_positions

while final != start_positions:
    
    path_to_home.append(final)
    final = hold_node[final]
    
path_to_home.append(initial_node)
path_to_home.reverse()


for i in range(len(path_to_home)):
    g.append(path_to_home[i][0])
    h.append(path_to_home[i][1])
    

L = merge(g,h)



img_copy = np.uint8(animated_map)


cv2.circle(img_copy, (start_positions[0],start_positions[1]), 3, (0,255,0), -1)
cv2.circle(img_copy, (goal_positions[0],goal_positions[1]), 3, (0,0,255), -1)


# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('PathFollower.mp4', fourcc, float(350), (250,600))

   
for i in range(len(L)):
    
    if i < len(L)-1:
        
        cv2.line(img_copy, L[i], L[i+1],(255,0,0), 3, None)
        
        cv2.imshow("Finished Trace", img_copy)
       
        
        cv2.waitKey(150)
        
        
        

# out.release()
cv2.destroyAllWindows()










    
            
            
            
            
            
            
            
            
            