X_LIMITS = (0,9999999999999999)
Y_LIMITS = (0,9999999999999999)

def parse_input_file(filename: str) -> tuple[list[list[str]],list[int]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
        idx = lines.index("\n")
        grid = lines[:idx]
        grid = list(map(lambda x: x.strip("\n"),grid))
        grid = list(map(list,grid))

        commands = lines[idx+1:]
        commands = ''.join(commands)
        list_commands = []
        for com in commands:
            match com:
                case "^":
                    list_commands.append(0)
                case ">":
                    list_commands.append(1)
                case "v":
                    list_commands.append(2)
                case "<":
                    list_commands.append(3)

    return (grid,list_commands)
        

def find_robot(grid: list[list[str]]) -> tuple[int,int]:
    global X_LIMITS, Y_LIMITS

    for y in range(Y_LIMITS[1]):
        for x in range(X_LIMITS[1]):
            if(grid[y][x] == "@"):
                return (x,y)

def move(grid: list[list[str]], pos: tuple[int,int], dir: tuple[int,int]) -> tuple[list[list[str]],tuple[int,int]]: # returns grid and object new position
    x = pos[0]
    y = pos[1]
    dx = dir[0]
    dy = dir[1]
    new_x = x + dx
    new_y = y + dy

    curr_obj = grid[y][x]
    new_obj = grid[new_y][new_x]

    if(new_obj == "#"):
        return (grid,(x,y))
    elif(new_obj == "."):
        grid[new_y][new_x] = curr_obj
        grid[y][x] = "."
        return (grid,(new_x,new_y))
    elif(new_obj == "O"):
        (grid,(temp_x,temp_y)) = move(grid,(new_x,new_y),dir)
        if(temp_x == new_x) and (temp_y == new_y):
            return (grid,(x,y))
        else:
            grid[new_y][new_x] = curr_obj
            grid[y][x] = "."
            return (grid,(new_x,new_y))

def gps_calculation(grid: list[list[str]]) -> int:

    global X_LIMITS, Y_LIMITS

    total = 0

    for y in range(Y_LIMITS[1]):
        for x in range(X_LIMITS[1]):
            if(grid[y][x] == "O"):
                total += (100 * y) + (1 * x)
    
    return total

if __name__ == "__main__":
    file_name = "input1.csv"
    (grid,commands) = parse_input_file(file_name)
    X_LIMITS = (0,len(grid[0]))
    Y_LIMITS = (0,len(grid))

    dx = [0,1,0,-1]
    dy = [-1,0,1,0]

    robot_x, robot_y = find_robot(grid)

    for command in commands:
        (grid,(robot_x,robot_y)) = move(grid, (robot_x,robot_y), (dx[command],dy[command]))
    
    for line in grid:
        print(' '.join(line))
    
    gps_value = gps_calculation(grid)
    print(gps_value)