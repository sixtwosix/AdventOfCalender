


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
    visited = [[False for i in range(COL_MAX)] for j in range(ROW_MAX)]
    stack.append([row_start,col_start])
    prev_val = -1
    previous = [row_start,col_start-1]
    found_goal = False
    # Iterate untill the stack is empty
    while (len(stack) > 0):
        current = stack.pop()        
        row = current[0]
        col = current[1]
        

        # if location is invalid
        if(col < 0) or (col >= COL_MAX) or (row < 0) or (row >= ROW_MAX):
            continue

        # already visited
        if(visited[row][col]) or (grid[row][col] == '.'):
            continue        
        
        
        current_val = int(grid[row][col])
        if(found_goal):
            prev_val = current_val -1
            previous = [row,col-1]
            found_goal = False


        neighbours = []
        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            neighbours.append([adjx,adjy])

        if(current_val != prev_val + 1) or ( previous not in neighbours):
            continue
        
        prev_val = current_val
        previous = current

        visited[row][col] = True
        
        if(current_val == goal_val) and ((row,col) not in goal_location):
            goal_location.add((row,col))
            found_goal = True
            print(f"Found a {goal_val} at location: {row} {col}")    

        # print(grid[row][col], end = " ")

        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            stack.append([adjx,adjy])
        
        
    
    return [goal for goal in goal_location]


if __name__ == "__main__":
    input_file = "test_input5.csv"

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
        print(start)
        trailhead_scores.append(len(DFS(start[0],start[1],grid,9)))
        
        

    print(trailhead_scores)
    # print(f"Found this many 9s: {len(final_locations)}")

    
