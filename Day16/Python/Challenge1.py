from heapq import heapify, heappop, heappush
import copy
from PIL import Image

X_LIMITS = (0,0)
Y_LIMITS = (0,0)

# node = (x,y,direction)
class Graph:
    def __init__(self,maze_grid: list[list[str]], graph: dict = {}):
        global X_LIMITS, Y_LIMITS
        self.graph = graph
        self.maze_grid = maze_grid     
        
        self.Y_MAX = len(maze_grid)
        self.X_MAX = len(maze_grid[0])
        X_LIMITS = (0,self.X_MAX)
        Y_LIMITS = (0,self.Y_MAX)
        
        for y in range(self.Y_MAX):
            for x in range(self.X_MAX):
                if(maze_grid[y][x] == "S") or (maze_grid[y][x] == "E") or (maze_grid[y][x] == "."):
                    self.graph[(x,y)] = {}
        
    def add_edge(self,node1, node2, weight,direction):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = (weight,direction)
    
    def shortest_distances(self, source: tuple):
        distances = {node: (float("inf"),-1,[node]) for node in self.graph}
        distances[source] = (0,1,[(source,1)])

        #((weight,direction,list_history_nodesDirr),(x,y))
        pq = [((0,1,[(source,1)]),source)]
        heapify(pq)
        
        visited = set()
        
        while(pq):
            (current_distance,curr_dir,curr_history_nodes),current_node = heappop(
                pq
            )
            
            if(current_node in visited):
                continue
            visited.add(current_node)
            
            dx = (0,1,0,-1)
            dy = (-1,0,1,0)
            curr_x = current_node[0]
            curr_y = current_node[1]
            # rotate left + step once = 1000 + 1
            if(self.maze_grid[curr_y+dy[(curr_dir-1)%4]][curr_x+dx[(curr_dir-1)%4]] != "#"):
                self.add_edge(current_node,(curr_x+dx[(curr_dir-1)%4],curr_y+dy[(curr_dir-1)%4]),1001,(curr_dir-1)%4)
            # rotate right + step once = 1000 + 1
            if(self.maze_grid[curr_y+dy[(curr_dir+1)%4]][curr_x+dx[(curr_dir+1)%4]] != "#"):
                self.add_edge(current_node,(curr_x+dx[(curr_dir+1)%4],curr_y+dy[(curr_dir+1)%4]),1001,(curr_dir+1)%4)
            # forward
            if(self.maze_grid[curr_y+dy[curr_dir]][curr_x+dx[curr_dir]] != "#"):
                self.add_edge(current_node,(curr_x+dx[curr_dir],curr_y+dy[curr_dir]),1,curr_dir)
            
            for neighbor, (weight, dirr) in self.graph[current_node].items():
                tentative_distance = current_distance + weight
                tentative_his_nodes = copy.deepcopy(curr_history_nodes)
                tentative_his_nodes.append((neighbor,dirr))
                if tentative_distance < distances[neighbor][0]:
                    distances[neighbor] = (tentative_distance, dirr, tentative_his_nodes)                    
                    heappush(pq, ((tentative_distance, dirr, tentative_his_nodes), neighbor))
        
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
    fileName = "test_input2.csv"
    
    maze_grid = parse_input_file(fileName)
    # for line in maze_grid:
    #     print(' '.join(line))
    maze_graph = Graph(maze_grid)
    
    distances = maze_graph.shortest_distances((1,len(maze_grid)-2))

    to_end = distances[(len(maze_grid)-2,1)]    

    for item in to_end[2]:
        x,y = item[0]
        dirr = item[1]
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
    
    for line in maze_grid:
        print(' '.join(line))
    
    print(f"Total cost: {to_end[0]}")

    print_image(maze_grid,f"{fileName.split(".")[0]}.bmp")