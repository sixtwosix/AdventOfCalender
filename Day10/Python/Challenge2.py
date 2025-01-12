# possible solution using BFS
#https://www.geeksforgeeks.org/print-paths-given-source-destination-using-bfs/



def BFS(row_start,col_start,grid,goal_val):

    # direction vectors
    dRow = [0, 1, 0, -1]
    dCol = [-1, 0, 1, 0]

    # maximum vals
    COL_MAX = len(grid)
    ROW_MAX = len(grid[0])

    # goal locations found
    goal_location = set()

    completed_paths = []
    stack = []
    visited = []
    stack.append([(row_start,col_start,0)])
    prev_val = -1
    found_goal = False
    # Iterate untill the stack is empty
    while (len(stack) > 0):
        # Bread first search from front
        path = stack.pop(0)
        last = path[len(path) -1 ]
        row = last[0]
        col = last[1]
        prev_val = last[2]
        
        if(prev_val == goal_val):
            completed_paths.append(last)
            
        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            if(adjy >= 0) and (adjy < COL_MAX) and (adjx >= 0) and (adjx < ROW_MAX):
                if(grid[adjx][adjy] != '.') and (int(grid[adjx][adjy]) == prev_val + 1):
                    newpath = path.copy()
                    newpath.append((adjx,adjy,int(grid[adjx][adjy])))
                    stack.append(newpath)

    return completed_paths


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
        trailhead_scores.append(len(BFS(start[0],start[1],grid,9)))

    # print(trailhead_scores)
    print(sum(trailhead_scores))


    
