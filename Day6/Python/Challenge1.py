# imports

def move_north(x,y,guard_map):
    guard_map[y][x] = 'X'
    y = y-1
    if(y >= 0):
        guard_map[y][x] = '^'
    
    return x,y,guard_map

def move_east(x,y,guard_map):
    guard_map[y][x] = 'X'
    x = x+1
    if(x < X_MAX):
        guard_map[y][x] = '>'
    
    return x,y,guard_map
    
def move_south(x,y,guard_map):
    guard_map[y][x] = 'X'
    y = y+1
    if(y < Y_MAX):
        guard_map[y][x] = 'v'
    
    return x,y,guard_map
    
def move_west(x,y,guard_map):
    guard_map[y][x] = 'X'
    x = x-1
    if(x >= 0):
        guard_map[y][x] = '<'
    
    return x,y,guard_map

def check_object(x, y, direction, guard_map):
    can_move = True
    match direction:
        # North
        case 'N':            
            if(y-1 >= 0) and (guard_map[y-1][x] == '#'):
                can_move = False
        # East
        case 'E':
            if(x+1 < X_MAX) and (guard_map[y][x+1] == '#'):
                can_move = False
        # South
        case 'S':
            if (y+1 < Y_MAX) and (guard_map[y+1][x] == '#'):
                can_move = False
        # West
        case 'W':
            if (x-1 >= 0) and (guard_map[y][x-1] == '#'):
                can_move = False
        
    return can_move

def find_starting(guard_map):
    for y in range(Y_MAX):
        for x in range(X_MAX):
            if(guard_map[y][x] == '^'):
                return x,y
            
def print_map(guard_map):
    for row in guard_map:
        print(row)
    print('================================================================')
    

if __name__ == "__main__":
    input_file = "input1.csv"
    
    with open(input_file,'r') as f:
        input_data = f.readlines()
        
    guard_map = []
    for line in input_data:
        guard_map.append(list(line.strip()))
    
    Y_MAX = len(guard_map)
    X_MAX = len(guard_map[0])
    
    print(f"Max Y value: {Y_MAX} -- Max X value: {X_MAX}")
    
    x,y = find_starting(guard_map)
    
    # Start facing North
    direction_facing = 'N'
    while((x < X_MAX) and (x >= 0) and (y < Y_MAX) and (y >= 0)):
        
        can_move = check_object(x,y,direction_facing,guard_map)
        
        if(can_move):
            match direction_facing:
                # North
                case 'N':
                    x,y,guard_map = move_north(x,y,guard_map)
                # East
                case 'E':
                    x,y,guard_map = move_east(x,y,guard_map)
                # South
                case 'S':
                    x,y,guard_map = move_south(x,y,guard_map)
                # West
                case 'W':
                    x,y,guard_map = move_west(x,y,guard_map)
        else:
            match direction_facing:
                # North
                case 'N':
                    direction_facing = 'E'
                # East
                case 'E':
                    direction_facing = 'S'
                # South
                case 'S':
                    direction_facing = 'W'
                # West
                case 'W':
                    direction_facing = 'N'
        
        # print_map(guard_map)
    
    count = 0
    for y in range(len(guard_map)):
        for x in range(len(guard_map)):
            if(guard_map[y][x] == 'X'):
                count += 1
    
    print(f"The guard made {count} moves")
    