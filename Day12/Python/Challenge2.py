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

def determine_side_counts(area):
    
    # do a left hand follower around the "structure" and count the amount of turns
    # if cant turn left or right but can turn around, add count +2

    # print(area)
    area_remaining = area.copy()

    temp_list = list(map(lambda x: x[1],area_remaining))
    x_limits = (min(temp_list)-1,max(temp_list)+1)
    temp_list = list(map(lambda y: y[0],area_remaining))
    y_limits = (min(temp_list)-1,max(temp_list)+1)
    # print(x_limits)
    # print(y_limits)

    x = area_remaining[0][1]
    y = area_remaining[0][0]-1
    dx = [1,1,1,0,-1,-1,-1,0]
    dy = [-1,0,1,1,1,0,-1,-1]
    # dx_new = [1,1,-1,-1]
    # dy_new = [-1,1,1,-1]

    
    direction = 0 # range[0,4]

    sides = 1

    queue = []
    queue.append((x,y))

    while (y >= y_limits[0] and y <= y_limits[1]) and (x >= x_limits[0] and x <= x_limits[1]):

        for i in range(8):
            #check where the next block is located.  based on the direction difference determine how much rotated = how many sides
            dir_new = (direction + i) % 8
            x_new = x + dx[dir_new]
            y_new = y + dy[dir_new]            
            x_new_minus1 = x+dx[dir_new-1]
            y_new_minus1 = y+dy[dir_new-1]
            
            if(check_area_contains(x_new,y_new,area_remaining) and not check_area_contains(x_new_minus1,y_new_minus1,area_remaining)):
                dir_new = dir_new - 1
                x = x + dx[dir_new]
                y = y + dy[dir_new]
                # if((x,y) in queue):
                if((x,y) == queue[0]):
                    x = -2
                else:
                    queue.append((x,y))
                
                    if(queue[-1][0]!= queue[-2][0]) and (queue[-1][1] != queue[-2][1]):
                        sides+=1
                        if(direction == dir_new):
                            sides+=1
                    #? Check if this works for E shape, figure out to add +2 when tunnel turns around
                    if(len(queue) >= 3) and (queue[-1][0] == queue[-3][0]) and (queue[-1][1] == queue[-3][1]):
                        sides+=2
                direction = dir_new                
                break

    # print(f"Sides: {sides}")
    # print(queue)
    
    return sides, queue

def check_area_contains(x,y,area):
    area_xy = list(map(lambda x: (x[1],x[0]),area))
    if((x,y) in area_xy):
        return  True
    else:
        return False

def determine_inside_blocks(surrounding_blocks, area):
    # TODO -> find the inside spots of the blocks and do the same follower
    area_xy = list(map(lambda x: (x[1],x[0]),area))
    outside_area = surrounding_blocks + area_xy
    # print(outside_area)
    
    temp_list = list(map(lambda x: x[1],outside_area))    
    x_limits = (min(temp_list)-1,max(temp_list)+1)
    np_x = np.array(temp_list)
    temp_list = list(map(lambda y: y[0],outside_area))
    np_y = np.array(temp_list)    
    y_limits = (min(temp_list)-1,max(temp_list)+1)

    # TODO: determine the empty blocks from the Crosstab created below
    df_res = pd.crosstab(np_x,np_y)
    # print(df_res)
    # * Only require one of the empty blocks inside each to start the sides search engine, can also itterate untill all inside blocks found    
    list_insides = []

    for x in range(x_limits[0]+2,x_limits[1]-2 + 1):
        for y in range(y_limits[0]+2,y_limits[1]-2 + 1):
            if(df_res[y][x]) == 0:
                list_insides.append((x,y))
    
    return list_insides
    
    
# TODO Fix issues with input3, some scenarios counting to much cause of inside counts and some missing counts on inside corners
# ? Maybe consider restructuring by adding count when direction changes with regards to 'N' 'E' 'S' 'W'
if __name__ == "__main__":
    input_file = "test_input3.csv"
    
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
            
            sides_count, outside_queue = determine_side_counts(area)
            inside_blocks = determine_inside_blocks(outside_queue,area)
            inside_count_total = 0
            while (len(inside_blocks) > 0):                        
                insides_count, inside_queue = determine_side_counts(inside_blocks)
                temp_insideBlocks = determine_inside_blocks(inside_queue,[])
                inside_count_total += insides_count
                for insideBlock in temp_insideBlocks:
                    inside_blocks.remove(insideBlock)
                # print(inside_blocks)
            
            for x in area:
                garden_coverage.remove(x)
        
            cost = len(area) * (sides_count + inside_count_total)
            print(f"Type {garden_type} : {len(area)} * {sides_count + inside_count_total} = {cost}")
            total_cost+=cost
    
    print(f"Total cost: {total_cost}")
    
    