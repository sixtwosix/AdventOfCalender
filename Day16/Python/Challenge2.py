from heapq import heapify, heappop, heappush
import copy
from PIL import Image

X_LIMITS = (0,0)
Y_LIMITS = (0,0)

# node = (x,y,direction)
class Graph:
    def __init__(self,maze_grid: list[list[str]]):
        global X_LIMITS, Y_LIMITS
        self.maze_grid = maze_grid     
        
        self.Y_MAX = len(maze_grid)
        self.X_MAX = len(maze_grid[0])
        X_LIMITS = (0,self.X_MAX)
        Y_LIMITS = (0,self.Y_MAX)
        
    # [(x,y,direction),.....]
    def dijkstra(self, starts : list[tuple[int]]) -> dict:
        delta = {0: (0,-1), 1:(1,0), 2:(0,1), 3:(-1,0)}
        
        distances = {}
        pq = []
        
        for x,y,dir in starts:
            distances[(x,y,dir)] = (0,[(x, y, dir)])
            heappush(pq, (0, x, y, dir, [(x, y, dir)]))
        
        while pq:
            (curr_weight, curr_x, curr_y, curr_direction, curr_history) = heappop(pq)
            
            if(distances[(curr_x,curr_y,curr_direction)][0] < curr_weight):
                # current distance recorded for this position and direction is smaller so skip the rest
                continue
            
            for next_direction in [(curr_direction-1)%4,(curr_direction+1)%4]:
                if(((curr_x,curr_y,next_direction) not in distances) 
                   or (distances[(curr_x,curr_y,next_direction)][0] >= curr_weight + 1000)):
                    temp_history = copy.deepcopy(curr_history)
                    temp_history.append((curr_x,curr_y,next_direction))
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
                temp_history = copy.deepcopy(curr_history)
                temp_history.append((next_x,next_y,curr_direction))
                distances[(next_x,next_y,curr_direction)] = (curr_weight + 1,temp_history)
                heappush(pq, (curr_weight + 1, next_x, next_y, curr_direction, temp_history))
        
        return distances
                        



def parse_input_file(fileName: str) -> list[list[str]]:
    with open(fileName, 'r') as f:
        maze_grid = f.readlines()
        maze_grid = list(map(lambda x: x.strip("\n"),maze_grid))
        maze_grid = list(map(list,maze_grid))
    
    return maze_grid

def print_image(grid: list[list[str]], fileName: str):
    
    global X_LIMITS, Y_LIMITS
    
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
                image.putpixel((x,y),(0,0,750))
                
    image.save(fileName)

if __name__ == "__main__":
    fileName = "input1.csv"
    
    maze_grid = parse_input_file(fileName)
    # for line in maze_grid:
    #     print(' '.join(line))
    maze_graph = Graph(maze_grid)
    
    dist_original = maze_graph.dijkstra([(1,len(maze_grid)-2,1)])
    final_value = float("inf")
    for direction in range(4):
        new_val = dist_original[(len(maze_grid)-2,1,direction)][0]
        final_value = min(final_value,new_val)
    # print(final_value)
    
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
