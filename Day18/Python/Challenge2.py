import heapq
import tqdm

def create_memory_grid(grid : list[list[str]], bad_pixels: list[tuple[int]], byte_count : int) -> list[list[str]]:
    
    for idx in range(byte_count):
        x,y = bad_pixels[idx]
        grid[y][x] = "#"
    
    return grid
    

def parse_file(fileName: str) -> list[tuple[int]]:
    with open(fileName, 'r') as f:
        bad_memory = f.readlines()
        bad_memory = list(map(lambda x: (int(x.split(",")[0]),int(x.split(",")[1])),bad_memory))
    return bad_memory

def dijkstra(grid : list[list[str]], start_byte : tuple[int], end_byte : tuple[int]):
    
    delta = {
        0: (0,-1),
        1: (1,0),
        2: (0,1),
        3: (-1,0)
    }
    
    pq = []
    visited = {}
        
    heapq.heappush(pq,(0,start_byte[0],start_byte[1]))
    visited[start_byte] = 0
    
    while pq:
        curr_weight,curr_x,curr_y = heapq.heappop(pq)
        
        if((curr_x,curr_y) == end_byte):
            return visited            
        
        if(grid[curr_y][curr_x] == "#") or not (0 <= curr_x < x_limits ) or not (0 <= curr_y < y_limits ):
            continue
        if(visited[(curr_x,curr_y)] < curr_weight):
            continue
        
        # visited[(curr_x,curr_y)] = []
        
        for i in range(4):
            dx, dy = delta[i]
            next_x, next_y = curr_x + dx, curr_y + dy            
            if(0 <= next_x < x_limits ) and (0 <= next_y < y_limits ) and (grid[next_y][next_x] != "#"):
                if((next_x,next_y) not in visited) or (visited[(next_x,next_y)] > curr_weight + 1):                                                        
                    visited[(next_x,next_y)] = curr_weight + 1
                    heapq.heappush(pq,(curr_weight + 1,next_x,next_y))                    
    
    return visited
    

if __name__ == "__main__":
    fileName = "input1.csv"
    bad_memory = parse_file(fileName)
    if(fileName.startswith("test")):
        x_limits = 6 + 1
        y_limits = 6 + 1
        byte_count = 12
    else:
        x_limits = 70 + 1
        y_limits = 70 + 1
        byte_count = 1024
        
    grid = [["." for x in range(x_limits)] for y in range(y_limits)]
    
    
    # for line in grid:
    #     print(" ".join(line))
    
    for memory in tqdm.tqdm(bad_memory):
        grid = create_memory_grid(grid,[memory],1)
    
        visited = dijkstra(grid,(0,0),(x_limits-1,y_limits-1))
        if((x_limits-1,y_limits-1) not in visited):
            # print(memory)
            break
        # least_steps = visited[(x_limits-1,y_limits-1)]
    
                
    # print(f"Shortest path is only {least_steps} steps")
    print(f"No destination exists after {memory} memory block got corrupted")
    
    