import glob
import contextlib
from PIL import Image
import os

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

def print_image(grid: list[list[str]], fileName: str):
    
    global X_LIMITS, Y_LIMITS
    
    image = Image.new('RGB', (X_LIMITS[1], Y_LIMITS[1]), color=(255,255,255))
    for y in range(Y_LIMITS[1]):
        for x in range(X_LIMITS[1]):
            obj = grid[y][x]
            if(obj == "#"):
                image.putpixel((x,y),(0,0,0))
            elif(obj == "@"):
                image.putpixel((x,y),(255,0,0))
            elif(obj == "O"):
                image.putpixel((x,y),(0,255,0))
                
    image.save(fileName)

if __name__ == "__main__":
    file_name = "test_input2.csv"
    (grid,commands) = parse_input_file(file_name)
    X_LIMITS = (0,len(grid[0]))
    Y_LIMITS = (0,len(grid))

    dx = [0,1,0,-1]
    dy = [-1,0,1,0]

    robot_x, robot_y = find_robot(grid)

    for idx, command in enumerate(commands):
        (grid,(robot_x,robot_y)) = move(grid, (robot_x,robot_y), (dx[command],dy[command]))
        ########## create the images #########################
        print_image(grid,f"./images/image_{idx}.bmp")
    
    for line in grid:
        print(' '.join(line))
    
    gps_value = gps_calculation(grid)
    print(gps_value)
    
    ########## create the gif #########################
    fp_in = f"{os.getcwd()}/images/image_*.bmp"
    fp_out = f"{os.getcwd()}/demo2.gif"
    
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in),key=len))
        
        # extract first image from iterator
        img = next(imgs)
        
        img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=150, loop=0)
        
    for f in sorted(glob.glob(fp_in),key=len):
        if os.path.exists(f):
            os.remove(f)
    
    
    