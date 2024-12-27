# imports

def move_north(x,y,guard_map):
    # guard_map[y][x] = 'X'
    y = y-1
    if(y >= 0):
        if(guard_map[y][x] != '+') and (guard_map[y][x] == '.'):
            guard_map[y][x] = '^'
        elif(guard_map[y][x] != '+') and (guard_map[y][x] != '.'):
            guard_map[y][x] = '+'
    
    return x,y,guard_map

def move_east(x,y,guard_map):
    # guard_map[y][x] = 'X'
    x = x+1
    if(x < X_MAX):
        if(guard_map[y][x] != '+') and (guard_map[y][x] == '.'):
            guard_map[y][x] = '>'
        elif(guard_map[y][x] != '+') and (guard_map[y][x] != '.'):
            guard_map[y][x] = '+'
    
    return x,y,guard_map
    
def move_south(x,y,guard_map):
    # guard_map[y][x] = 'X'
    y = y+1
    if(y < Y_MAX):
        if(guard_map[y][x] != '+') and (guard_map[y][x] == '.'):
            guard_map[y][x] = 'v'
        elif(guard_map[y][x] != '+') and (guard_map[y][x] != '.'):
            guard_map[y][x] = '+'
    
    return x,y,guard_map
    
def move_west(x,y,guard_map):
    # guard_map[y][x] = 'X'
    x = x-1
    if(x >= 0):
        if(guard_map[y][x] != '+') and (guard_map[y][x] == '.'):
            guard_map[y][x] = '<'
        elif(guard_map[y][x] != '+') and (guard_map[y][x] != '.'):
            guard_map[y][x] = '+'
    
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
    

# def check_if_90_degrees(x, y, direction, guard_map):
#     is_90_degrees = False
#     match direction:
#         # North
#         case 'N':            
#             if(y-1 >= 0) and (guard_map[y][x] == '>'):
#                 is_90_degrees = True
#                 # guard_map[y][x] = "+"
#                 return is_90_degrees, guard_map, (x,y-1)
#         # East
#         case 'E':
#             if(x+1 < X_MAX) and (guard_map[y][x] == 'v'):
#                 is_90_degrees = True
#                 # guard_map[y][x] = "+"
#                 return is_90_degrees, guard_map, (x+1,y)
#         # South
#         case 'S':
#             if (y+1 < Y_MAX) and (guard_map[y][x] == '<'):
#                 is_90_degrees = True
#                 # guard_map[y][x] = "+"
#                 return is_90_degrees, guard_map, (x,y+1)
#         # West
#         case 'W':
#             if (x-1 >= 0) and (guard_map[y][x] == '^'):
#                 is_90_degrees = True
#                 # guard_map[y][x] = "+"
#                 return is_90_degrees, guard_map, (x-1,y)
    
#     return is_90_degrees, guard_map, (-1,-1)
    

def check_distant_loop(x,y,direction, guard_map):
    is_distant_loop = False

    match direction:
        # North
        case 'N':    
            for j in range(x,X_MAX):
                if(guard_map[y][j] == ">") :
                    is_distant_loop = True
                    return is_distant_loop, (x,y-1)
                # elif((j+1 < X_MAX) and (guard_map[y][j+1] == "#") and (guard_map[y+1][j] == "v")):
                elif(j+1 < X_MAX) and (guard_map[y][j+1] == "#"):
                    temp_list = [guard_map[a][j] for a in range(y,-1,-1)]
                    for a in temp_list:
                        if(a == "+"):
                            continue
                        elif( a == "v"):
                            is_distant_loop = True
                            return is_distant_loop, (x,y-1,direction)        
                        else:
                            break
                    
        # East
        case 'E':
            for i in range(y,Y_MAX):
                if(guard_map[i][x] == "v"):
                    is_distant_loop = True
                    return is_distant_loop, (x+1,y)
                # elif((i+1 < Y_MAX) and (guard_map[i+1][x] == "#") and (guard_map[i][x+1] == "<")):
                elif(i+1 < Y_MAX) and (guard_map[i+1][x] == "#"):
                    temp_list = [guard_map[i][a] for a in range(x,-1,-1)]
                    for a in temp_list:
                        if(a == "+"):
                            continue
                        elif( a == "<"):
                            is_distant_loop = True
                            return is_distant_loop, (x+1,y,direction)
                        else:
                            break
                    
        # South
        case 'S':
            for j in range(0,x):
                if(guard_map[y][j] == "<"):
                    is_distant_loop = True
                    return is_distant_loop, (x,y+1)
                # elif((j-1 >= 0) and (guard_map[y][j-1] == "#") and (guard_map[y-1][j] == "^")):
                elif(j-1 >= 0) and (guard_map[y][j-1] == "#"):
                    temp_list = [guard_map[a][j] for a in range(y,Y_MAX)]
                    for a in temp_list:
                        if(a == "+"):
                            continue
                        elif( a == "^"):
                            is_distant_loop = True
                            return is_distant_loop, (x,y+1,direction)
                        else:
                            break
                    
        # West
        case 'W':
            for i in range(0,y):
                if(guard_map[i][x] == "^"):
                    is_distant_loop = True
                    return is_distant_loop, (x-1,y)
                # elif((i-1 >= 0) and (guard_map[i-1][x] == "#") and (guard_map[i][x+1] == ">")):
                elif(i-1 >= 0) and (guard_map[i-1][x] == "#"):
                    temp_list = [guard_map[i][a] for a in range(x,X_MAX)]
                    for a in temp_list:
                        if(a == "+"):
                            continue
                        elif( a == ">"):
                            is_distant_loop = True
                            return is_distant_loop, (x-1,y,direction)
                        else:
                            break                    
                    

    return is_distant_loop, (-1,-1)
    


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
    
    new_object_placement = 0
    new_object_location_hist = set()

    # Start facing North
    direction_facing = 'N'
    while((x < X_MAX) and (x >= 0) and (y < Y_MAX) and (y >= 0)):

        # if(x == 6 and y == 7):
        #     print
        
        # if(guard_map[y][x] in ["<",">","^","v","+"]):
            # is_90_degrees,guard_map,new_object_location = check_if_90_degrees(x,y,direction_facing,guard_map)
            # if(is_90_degrees):
            #     new_object_placement += 1
            #     # print_map(guard_map)                
            #     if not(new_object_location in new_object_location_hist):
            #         with open("2_out.csv", 'a') as f:
            #             f.writelines(f"({new_object_location[0]},{new_object_location[1]})\n")
            #     new_object_location_hist.add(new_object_location)
            # else:
        is_distant_loop,new_object_location = check_distant_loop(x,y,direction_facing,guard_map)
        if(is_distant_loop):
            new_object_placement += 1                    
            # print_map(guard_map)                    
            if not(new_object_location in new_object_location_hist):
                with open("2_out.csv", 'a') as f:
                    f.writelines(f"({new_object_location[0]},{new_object_location[1]})\n")
            new_object_location_hist.add(new_object_location)
            # print(new_object_location)
                
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
                    guard_map[y][x] = "+"
                    x,y,guard_map = move_east(x,y,guard_map)
                # East
                case 'E':
                    direction_facing = 'S'
                    guard_map[y][x] = "+"
                    x,y,guard_map = move_south(x,y,guard_map)
                # South
                case 'S':
                    direction_facing = 'W'
                    guard_map[y][x] = "+"
                    x,y,guard_map = move_west(x,y,guard_map)
                # West
                case 'W':
                    direction_facing = 'N'
                    guard_map[y][x] = "+"
                    x,y,guard_map = move_north(x,y,guard_map)       
        
        
        # print_map(guard_map)   
    
    
    print(f"We can place an object on {new_object_placement} places to make infinite loops")

    print(f"We can place an object on {len(new_object_location_hist)} places to make infinite loops")
    