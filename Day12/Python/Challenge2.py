

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

    print(area)
    area_remaining = area.copy()

    temp_list = list(map(lambda x: x[1],area_remaining))
    x_limits = (min(temp_list)-1,max(temp_list)+1)
    temp_list = list(map(lambda y: y[0],area_remaining))
    y_limits = (min(temp_list)-1,max(temp_list)+1)
    print(x_limits)
    print(y_limits)

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

            if(check_area_contains(x_new,y_new,area_remaining)):
                dir_new = dir_new - 1
                x = x + dx[dir_new]
                y = y + dy[dir_new]
                if((x,y) in queue):
                    x = -2
                else:
                    queue.append((x,y))
                # if(direction != dir_new):
                    if(queue[-1][0]!= queue[-2][0]) and (queue[-1][1] != queue[-2][1]):
                        # TODO: Figure out the 3rd shape why its missing some sides
                        sides+=1
                direction = dir_new                
                break

    print(f"Sides: {sides}")
            
            


        

def check_area_contains(x,y,area):
    area_xy = list(map(lambda x: (x[1],x[0]),area))
    if((x,y) in area_xy):
        return  True
    else:
        return False

    
def determine_inside_side_counts():

    # find the inside spots of the blocks and do the same follower

    print(area)

if __name__ == "__main__":
    input_file = "test_input1.csv"
    
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
            
            determine_side_counts(area)
            
            for x in area:
                garden_coverage.remove(x)
        
            cost = len(area) * len(circumference)
            print(f"Type {garden_type} : {len(area)} * {len(circumference)} = {cost}")
            total_cost+=cost
    
    print(f"Total cost: {total_cost}")
    
    