from itertools import product
from operator import gt, lt
import re

# y_limits = (0,7)
# x_limits = (0,11)
y_limits = (0,103)
x_limits = (0,101)
    
duration = 100    

def parse_input_file(input_file_name):
    regex_string = "p=(\d+),(\d+) v=(-*\d+),(-*\d+)"
    
    list_robots = []
    
    with open(input_file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            x = re.match(regex_string,line)
            list_robots.append([
                int(x.group(1)),
                int(x.group(2)),
                int(x.group(3)),
                int(x.group(4))
            ])
        
    return list_robots

def determine_robot_poisiton(robot):
    
    global y_limits, x_limits, duration
    
    x = robot[0]
    y = robot[1]
    dx = robot[2]
    dy = robot[3]
    
    for i in range(duration) :
        new_x = x + dx
        new_y = y + dy
        if(new_x >= x_limits[1]):
            new_x = new_x-x_limits[1]
        if(new_x < x_limits[0]):
            new_x = new_x+x_limits[1]
        if(new_y >= y_limits[1]):
            new_y = new_y-y_limits[1]
        if(new_y < y_limits[0]):
            new_y = new_y+y_limits[1]
    
        x = new_x
        y = new_y
    
    return (x,y)

def quadrants_calculation(robots_pos):
    
    # x_line = round(x_limits[1]/2)-1
    # y_line = round(y_limits[1]/2)-1
    x_line = x_limits[1] // 2
    y_line = y_limits[1] // 2
    
    # totals = [0,0,0,0]
    totals = [[],[],[],[]]
    
    for pos in robots_pos:
        if(pos[0] < x_line):
            if(pos[1] < y_line):
                # totals[0] = totals[0] + 1
                totals[0].append(pos)
            elif(pos[1] > y_line):
                # totals[2] = totals[2] + 1
                totals[2].append(pos)
        elif(pos[0] > x_line):
            if(pos[1] < y_line):
                # totals[1] = totals[1] + 1
                totals[1].append(pos)
            elif(pos[1] > y_line):
                # totals[3] = totals[3] + 1 
                totals[3].append(pos)
    
    return totals       

if __name__ == "__main__":
    input_file_name = "input1.csv"
    list_robots = parse_input_file(input_file_name)
    
    final_pos = list(map(determine_robot_poisiton,list_robots))
    # final_pos.sort()
    # print(final_pos)
    
    robots = []
    for robot in list_robots:
        updated_row = (robot[1] + robot[3] * 100) % y_limits[1]
        updated_col = (robot[0] + robot[2] * 100) % x_limits[1]
        robots.append((updated_col, updated_row))
    
    # c = [item for item in final_pos if item not in robots]
    # print(c)
    # c = [item for item in robots if item not in final_pos]
    # print(c)
    
    quadrant_totals = quadrants_calculation(final_pos)
    # print(quadrant_totals)
    
    row_boundary = y_limits[1] // 2
    col_boundary = x_limits[1] // 2

    test_quads = []
    for row_op, col_op in product([lt, gt], repeat=2):
        quad = [
                r
                for r in final_pos
                if row_op(r[1], row_boundary) and col_op(r[0], col_boundary)
            ]
        test_quads.append(quad)
        
    # print(test_quads)
    
    for i in range(4):
        c = [item for item in quadrant_totals[i] if item not in test_quads[i]]
        print(f"mine not in example {i}")
        print(len(quadrant_totals[i]),len(test_quads[i]))
        print(c)
        print()
    
    for i in range(4):
        c = [item for item in test_quads[i] if item not in quadrant_totals[i]]
        print(f"example not in mine{i}")
        print(len(quadrant_totals[i]),len(test_quads[i]))
        print(c)
        print()
    
    total = 1
    for val in quadrant_totals:        
        if(len(val) != 0):
            total = total*len(val)
    
    print(total)
    