import re
from PIL import Image
from tqdm import tqdm

# y_limits = (0,7)
# x_limits = (0,11)
y_limits = (0,103)
x_limits = (0,101)
    
duration = 1  

def parse_input_file(input_file_name):
    regex_string = "p=(\d+),(\d+) v=(-*\d+),(-*\d+)"
    
    list_robots = []
    
    with open(input_file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            x = re.match(regex_string,line)
            list_robots.append([
                int(x.group(1)),
                int(x.group(2)),
                int(x.group(3)),
                int(x.group(4))
            ])
        
    return list_robots

def determine_robot_poisiton(robot):
    
    global y_limits, x_limits, duration

    updated_row = (robot[1] + robot[3] * duration) % y_limits[1]
    updated_col = (robot[0] + robot[2] * duration) % x_limits[1]

    return (updated_col,updated_row)       

def check_xmas_tree(robots_pos : list, counter : int):
    
    grid = [ [0 for x in range(x_limits[1])] for y in range(y_limits[1])]
    
    image = Image.new('1', (x_limits[1], y_limits[1]), color=0)
    
    for pos in robots_pos:
        grid[pos[1]][pos[0]] = 1
        image.putpixel((pos[0],pos[1]),1)
       
    for y in range(y_limits[1]):
        for x in range(x_limits[1]):
            
            if(grid[y][x] == 1):                
                if(y+1 < y_limits[1] ) and (x+1 < x_limits[1]) and (x-1 >= 0 ) and (grid[y+1][x+1] == 1) and (grid[y+1][x-1] == 1):
                    if(y+2 < y_limits[1] ) and (x+2 < x_limits[1]) and (x-2 >= 0 ) and (grid[y+1][x+2] == 1) and (grid[y+1][x-2] == 1):
                        if(y+3 < y_limits[1] ) and (x+3 < x_limits[1]) and (x-3 >= 0 ) and (grid[y+1][x+3] == 1) and (grid[y+1][x-3] == 1):
                            ## prints the possible images
                            image.save(f"./images/file_{counter}.bmp")
                            return True
    
    return False
                    

if __name__ == "__main__":
    
    input_file_name = "input1.csv"
    list_robots = parse_input_file(input_file_name)
    
    for i in tqdm(range(10000)):
        duration = i + 1
        final_pos = list(map(determine_robot_poisiton,list_robots))
        if(check_xmas_tree(final_pos,i)):
            print("==========================================================================================")
            print(f"Possible shape at {i}")
    