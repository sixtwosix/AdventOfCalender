import pandas as pd
import numpy as np

# use BFS to find each similar object of letter in list
def breadth_first_search(row,col,garden,garden_type):
    
    dRow = [0, 1, 0, -1]
    dCol = [-1, 0, 1, 0]

    # maximum vals
    COL_MAX = len(garden)
    ROW_MAX = len(garden[0])
    
    queue = []
    
    # current area
    curr_area = []
    curr_circumference = []
    curr_block = (row,col,garden[row][col])
    queue.append(curr_block)
    
    while queue:
        curr_block = queue.pop(0)
        row = curr_block[0]
        col = curr_block[1]        
        
        if((row,col,garden[row][col]) in curr_area):
            continue
        
        # count each letter 'X' that has a non 'X' letter next to it
        # thus have a 'Y' next to 'X'
        if(curr_block[2] != garden_type):
            curr_circumference.append(curr_block)
            continue
        
        # count each letter 'X' for the area
        # if(curr_block[2] == garden_type):
        curr_area.append(curr_block)        

        # check only directions vertical and horizontal
        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            
            # check if new is inside the grid
            if(adjy >= 0) and (adjy < COL_MAX) and (adjx >= 0) and (adjx < ROW_MAX):
                queue.append((adjx,adjy,garden[adjx][adjy]))
            else:
                curr_circumference.append((adjx,adjy,'.'))
    
    return curr_area,curr_circumference

# * Perfom a scanning algorithm from all 4 sides and determine if there are changes from previous row to count sides
def scanning_side_counts(area):
    area_xy = list(map(lambda x: (x[1],x[0]),area))
    temp_list = list(map(lambda x: x[1],area))
    x_limits = (min(temp_list),max(temp_list))
    temp_list = list(map(lambda y: y[0],area))
    y_limits = (min(temp_list),max(temp_list))

    sides = 0

    # Scan from top Down
    sides += scan_line_by_line(y_limits[0],y_limits[1]+1,1,area_xy,0)

    # Scan from bottom Up
    sides += scan_line_by_line(y_limits[1],y_limits[0]-1,-1,area_xy,0)    

    # Scan from Left to Right
    sides += scan_line_by_line(x_limits[0],x_limits[1]+1,1,area_xy,1)
    
    # Scan from Right to Left
    sides += scan_line_by_line(x_limits[1],x_limits[0]-1,-1,area_xy,1)
        
    return sides


def scan_line_by_line(lower_limit,upper_limit,increment,area_xy,elemenet_nr):
    prev_line = []
    sides = 0
    for b in range(lower_limit,upper_limit,increment):
        prev_a = list(map(lambda x: x[elemenet_nr],prev_line))
        curr_line = list(filter(lambda coordinate: coordinate[(elemenet_nr+1)%2] == b,area_xy ))
        curr_a = list(map(lambda x: x[elemenet_nr],curr_line))
        diff_a = list(set(prev_a).symmetric_difference(curr_a))
        diff_a = list(set(diff_a).intersection(curr_a))
        diff_a.sort()
        # print(diff_x)
        if(diff_a != []):
            sides += check_gaps_inline(diff_a) + 1

        prev_line = curr_line

    return sides

def check_gaps_inline(line):    
    res = list(map(lambda a, b: b - a, line,line[1:]))
    res = list(map(lambda a: 0 if abs(a) == 1 else 1,res))
    return sum(res)

if __name__ == "__main__":
    input_file = "input1.csv"
    
    with open(input_file, 'r') as f:
        garden = f.readlines()
    
    garden = list(map(str.strip,garden))
    garden = list(map(list,garden))
    
    garden_coverage = []

    Y_MAX = len(garden)
    X_MAX = len(garden[0])
    
    print("Garden coverage")
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            garden_coverage.append((i,j,garden[i][j]))
    
    garden_types = {i:sum(garden,[]).count(i) for i in sum(garden,[])}
    print(garden_types)
        
    total_cost = 0
        
    for garden_type in list(garden_types.keys()):        
        while True:            
            remaining = list(filter(lambda x: x[2] == garden_type,garden_coverage))
            if(len(remaining) == 0):
                break
            
            start_x = remaining[0][0]
            start_y = remaining[0][1]
        
            area,circumference = breadth_first_search(start_x,start_y,garden,garden_type)
            
            sides_count = scanning_side_counts(area)
            
            for x in area:
                garden_coverage.remove(x)
        
            cost = len(area) * (sides_count)
            print(f"Type {garden_type} : {len(area)} * {sides_count} = {cost}")
            total_cost+=cost
    
    print(f"Total cost: {total_cost}")
    
    