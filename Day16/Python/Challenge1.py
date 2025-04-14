from heapq import heapify, heappop, heappush

# node = (x,y,direction)
class Graph:
    def __init__(self,maze_grid: list[list[str]], graph: dict = {}):
        self.graph = graph
        self.maze_grid = maze_grid     
        
        self.Y_MAX = len(maze_grid)
        self.X_MAX = len(maze_grid[0])
        
        # dx = (0,1,0,-1)
        # dy = (1,0,-1,0)
        
        # self.start_node = (-1,-1,1)
        # self.end_node = (-1,-1,1)
        
        for y in range(self.Y_MAX):
            for x in range(self.X_MAX):
                if(maze_grid[y][x] == "S") or (maze_grid[y][x] == "E") or (maze_grid[y][x] == "."):
                    self.graph[(x,y)] = {}    
            
        # queue = [self.start_node]
        # visited = set()
        
        # while queue:
        #     # node = (x,y,dir)

        #     curr_node = queue.pop(0)
        #     curr_x = curr_node[0]
        #     curr_y = curr_node[1]
        #     curr_dir = curr_node[2]
        #     visited.add(curr_node)
            
        #     for i in range(4):
        #         new_x = curr_x + dx[i]
        #         new_y = curr_y + dy[i]
        #         if(maze_grid[new_x][new_y] == ".") or (maze_grid[new_x][new_y] == "E") or (maze_grid[new_x][new_y] == "S"):
        #             new_dir = i
        #             new_node = (new_x,new_y,new_dir)
        #             if(new_node not in visited) and (new_dir-curr_dir != 2):
        #                 dir_diff = (new_dir-curr_dir)%2 
        #                 weight = 1 if (dir_diff == 0) else dir_diff*1000
        #                 self.add_edge(curr_node,new_node,weight)
        #                 queue.append(new_node)                   
            
        
    def add_edge(self,node1, node2, weight,direction):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = (weight,direction)
    
    def shortest_distances(self, source: tuple):
        distances = {node: (float("inf"),-1) for node in self.graph}
        distances[source] = 0

        #((weight,direction),(x,y))
        pq = [((0,1),source)]
        heapify(pq)
        
        visited = set()
        
        while(pq):
            (current_distance,curr_dir),current_node = heappop(
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
                if tentative_distance < distances[neighbor][0]:
                    distances[neighbor] = (tentative_distance, dirr)
                    heappush(pq, ((tentative_distance, dirr), neighbor))
        
        return distances



def parse_input_file(fileName: str) -> list[list[str]]:
    with open(fileName, 'r') as f:
        maze_grid = f.readlines()
        maze_grid = list(map(lambda x: x.strip("\n"),maze_grid))
        maze_grid = list(map(list,maze_grid))
    
    return maze_grid

if __name__ == "__main__":
    fileName = "input1.csv"
    
    maze_grid = parse_input_file(fileName)
    for line in maze_grid:
        print(' '.join(line))
    maze_graph = Graph(maze_grid)
    print()
    
    distances = maze_graph.shortest_distances((1,len(maze_grid)-2))
    print()
    to_end = distances[(len(maze_grid)-2,1)]
    print(to_end)
    