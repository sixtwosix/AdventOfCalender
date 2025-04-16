from heapq import heappop, heappush
from PIL import Image
import os
import contextlib
import glob

X_LIMITS = (0,0)
Y_LIMITS = (0,0)

# node = (x,y,direction)
class Graph:
    def __init__(self,maze_grid: list[list[str]], bool_gif: bool):
        global X_LIMITS, Y_LIMITS
        self.maze_grid = maze_grid     
        
        self.Y_MAX = len(maze_grid)
        self.X_MAX = len(maze_grid[0])
        X_LIMITS = (0,self.X_MAX)
        Y_LIMITS = (0,self.Y_MAX)

        self.img_idx = 0
        self.bool_gif = bool_gif
        
    # [(x,y,direction),.....]
    def dijkstra(self, starts : list[tuple[int]]) -> dict:
        delta = {0: (0,-1), 1:(1,0), 2:(0,1), 3:(-1,0)}
        
        distances = {}
        pq = []
        
        for x,y,dir in starts:
            distances[(x,y,dir)] = (0,[(x, y, dir)])
            heappush(pq, (0, x, y, dir, [(x, y, dir)]))
        
        idx = 0
        while pq:
            (curr_weight, curr_x, curr_y, curr_direction, curr_history) = heappop(pq)
            
            if(distances[(curr_x,curr_y,curr_direction)][0] < curr_weight):
                # current distance recorded for this position and direction is smaller so skip the rest
                continue
            
            for next_direction in [(curr_direction-1)%4,(curr_direction+1)%4]:
                if(((curr_x,curr_y,next_direction) not in distances) 
                   or (distances[(curr_x,curr_y,next_direction)][0] >= curr_weight + 1000)):
                    temp_history = curr_history + [(curr_x,curr_y,next_direction)]
                    distances[(curr_x,curr_y,next_direction)] = (curr_weight + 1000,temp_history)
                    heappush(pq,(curr_weight+1000, curr_x, curr_y, next_direction, temp_history))
            
            dx,dy = delta[curr_direction]
            next_x = curr_x + dx
            next_y = curr_y + dy
            
            if( (0 <= next_x < self.X_MAX) and
                (0 <= next_y < self.Y_MAX) and
                (self.maze_grid[next_y][next_x] != "#") and
                (   
                    (next_x,next_y,curr_direction) not in distances 
                    or distances[(next_x,next_y,curr_direction)][0] >= curr_weight + 1
                )   
            ):
                temp_history = curr_history + [(next_x,next_y,curr_direction)]
                distances[(next_x,next_y,curr_direction)] = (curr_weight + 1,temp_history)
                heappush(pq, (curr_weight + 1, next_x, next_y, curr_direction, temp_history))
            if(self.bool_gif):
                print_image(self.maze_grid,f"./images/image_{idx}.bmp",distances,pq)
                idx+=1
        
        self.img_idx = idx
        return distances
                        



def parse_input_file(fileName: str) -> list[list[str]]:
    with open(fileName, 'r') as f:
        maze_grid = f.readlines()
        maze_grid = list(map(lambda x: x.strip("\n"),maze_grid))
        maze_grid = list(map(list,maze_grid))
    
    return maze_grid

def print_image(grid: list[list[str]], fileName: str, visited: dict, queue: list):
    
    global X_LIMITS, Y_LIMITS
    
    visited = list(visited.keys())
    visited = list(map(lambda x: (x[0],x[1]), visited))

    queue = list(map(lambda x: (x[1],x[2]), queue))

    image = Image.new('RGB', (X_LIMITS[1], Y_LIMITS[1]), color=(255,255,255))
    for y in range(Y_LIMITS[1]):
        for x in range(X_LIMITS[1]):
            obj = grid[y][x]
            if(obj == "#"):
                image.putpixel((x,y),(0,0,0))
            elif(obj == "E"):
                image.putpixel((x,y),(255,0,0))
            elif(obj == "S"):
                image.putpixel((x,y),(0,255,0))
            elif(obj == "^") or (obj == ">") or (obj == "<") or (obj == "v"):
                image.putpixel((x,y),(255,128,0))
            elif((x,y) in queue):
                image.putpixel((x,y),(255,255,70)) # light yellow
            elif((x,y) in visited):
                image.putpixel((x,y),(102,102,255)) # very light green            
                
    image.save(fileName)

if __name__ == "__main__":
    fileName = "input1.csv"
    
    maze_grid = parse_input_file(fileName)
    # for line in maze_grid:
    #     print(' '.join(line))
    maze_graph = Graph(maze_grid,True)
    
    dist_original = maze_graph.dijkstra([(1,len(maze_grid)-2,1)])
    final_value = float("inf")
    for direction in range(4):
        new_val = dist_original[(len(maze_grid)-2,1,direction)][0]
        final_value = min(final_value,new_val)
    print(final_value)

    dist_original_path = dist_original[(len(maze_grid)-2,1,direction)][1]

    for item in dist_original_path:
        x = item[0]
        y = item[1]
        dirr = item[2]
        obj = maze_grid[y][x]
        if(obj == "."):
            if(dirr == 0):
                maze_grid[y][x] = "^"
            elif(dirr == 1):
                maze_grid[y][x] = ">"
            elif(dirr == 2):
                maze_grid[y][x] = "v"
            elif(dirr == 3):
                maze_grid[y][x] = "<"
    
    for i in range(1,50):
        print_image(maze_grid,f"./images/image_{maze_graph.img_idx+i}.bmp",dist_original,[])

    ########## create the gif #########################
    fp_in = f"{os.getcwd()}/images/image_*.bmp"
    fp_out = f"{os.getcwd()}/{fileName.split(".")[0]}.gif"
    
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in),key=len))
        
        # extract first image from iterator
        img = next(imgs)
        
        img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=25, loop=1)
        
    for f in sorted(glob.glob(fp_in),key=len):
        if os.path.exists(f):
            os.remove(f)
    
    ########## create the gif  end #########################

    maze_graph.bool_gif = False

    dist_reverse = maze_graph.dijkstra([(len(maze_grid)-2,1,direction) for direction in range(4)] ) 
    
    flip = {0:2,1:3,2:0,3:1}
    locations = set()
    for y in range(len(maze_grid)):
        for x in range(len(maze_grid[0])):
            for direction in range(4):
                state_from_start = (x,y,direction)
                state_from_end = (x,y,flip[direction])
                
                if( (state_from_start in dist_original) and 
                    (state_from_end in dist_reverse)    ):
                    sum_orignal_reverse = dist_original[state_from_start][0] + dist_reverse[state_from_end][0]
                    if(sum_orignal_reverse == final_value):
                        locations.add((x,y))
                        
    # print(locations)        
    print(len(locations))

    for item in locations:
        x,y = item[0],item[1]
        maze_grid[y][x] = "O"
    
    for line in maze_grid:
        print(' '.join(line))
