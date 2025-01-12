


def DFS(row_start,col_start,grid,goal_val):

    # direction vectors
    dRow = [0, 1, 0, -1]
    dCol = [-1, 0, 1, 0]

    # maximum vals
    COL_MAX = len(grid)
    ROW_MAX = len(grid[0])

    # goal locations found
    goal_location = set()

    stack = []
    visited = []
    stack.append([row_start,col_start])
    prev_val = -1
    found_goal = False
    # Iterate untill the stack is empty
    while (len(stack) > 0):
        current = stack.pop()        
        row = current[0]
        col = current[1]

        # already visited
        if((row,col) in visited) or (grid[row][col] == '.'):
            continue        
        
        
        current_val = int(grid[row][col])
        if(found_goal and current_val-prev_val != 1):
            prev_val = current_val -1
            found_goal = False

        visited.append((row,col))
        
        if(current_val == goal_val) and ((row,col) not in goal_location):
            goal_location.add((row,col))
            found_goal = True
            # print(f"Found a {goal_val} at location: {row} {col}")    
        else:
            prev_val = current_val

            for i in range(4):
                adjx = row + dRow[i]
                adjy = col + dCol[i]
                # check if next possible cells are valid
                if(adjy >= 0) and (adjy < COL_MAX) and (adjx >= 0) and (adjx < ROW_MAX):
                    if(grid[adjx][adjy] != '.') and (int(grid[adjx][adjy]) == prev_val + 1):
                        stack.append([adjx,adjy])
        
        
    
    return [goal for goal in goal_location]


if __name__ == "__main__":
    input_file = "input1.csv"

    grid = []

    with open(input_file, 'r') as f:
        grid = f.readlines()
    
    grid = list(map(str.strip,grid))    
    grid = list(map(list ,grid))

    starting_locations = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if(grid[r][c] == '0'):
                starting_locations.add((r,c))
    
    trailhead_scores = []

    for start in starting_locations:
        # print(start)
        trailhead_scores.append(len(DFS(start[0],start[1],grid,9)))

    # print(trailhead_scores)
    print(sum(trailhead_scores))


    
