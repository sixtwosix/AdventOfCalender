

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
    
    