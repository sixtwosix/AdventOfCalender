import heapq
import sys

# def dijkstra (grid: list[list[str]], start: tuple[int], end: tuple[int], cheat_count: int, start_weight: int, cheat_distance: dict) -> tuple[dict]:
def dijkstra (grid: list[list[str]], start: tuple[int], end: tuple[int], start_weight: int) -> tuple[dict]:
    
    max_cheat = 2
    
    delta = {
        0:(0,-1), # north
        1:(1,0), # east
        2:(0,1), # south
        3:(-1,0)  # west
    }
    
    distance = {}  
    x,y = start
    pq = []    
    
    heapq.heappush(pq,(start_weight,x,y))
    distance[(start[0],start[1])] = (start_weight,start)
    
    while pq:
        
        (weight, x ,y) = heapq.heappop(pq)
        
        if((x,y) == end):
            return distance
        
        if(distance[(x,y)][0] < weight):
            continue
        
        for i in range(4):
            # normal section
            dx,dy = delta[i]
            new_x = x + dx
            new_y = y + dy
            if(0 <= new_y < len(grid)) and (0 <= new_x < len(grid[0])) and (grid[new_y][new_x] != "#"):
                if((new_x,new_y) not in distance) or (distance[(new_x,new_y)][0] > weight + 1):
                    distance[(new_x,new_y)] = (weight + 1,(x,y))
                    heapq.heappush(pq,(weight+1,new_x,new_y))
    
    return distance    

        
def start_end_find(grid: list[list[str]]) -> tuple[tuple[int],tuple[int]]:
    
    start = (-1,-1)
    end = (-1,-1)
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if(grid[y][x] == 'S'):
                start = (x,y)
            if(grid[y][x] == 'E'):
                end = (x,y)
    
    return (start,end)

def parse_file(fileName : str) -> list[list[str]]:
    with open(fileName, 'r') as f:
        grid = f.readlines()
        grid = list(map(str.strip,grid))
        grid = list(map(list,grid))
    return grid

def manhattan_distance(p1: tuple[int], p2: tuple[int]):
    x = abs(p1[0]-p2[0])
    y = abs(p1[1]-p2[1])
    return x + y


if __name__ == "__main__":
    fileName = "input1.csv"       
    
    grid = parse_file(fileName)
    
    if(fileName.startswith("test")):
        # test case
        faster_than = 50
        cheat_count_max = 20
    else:
        # prod case
        faster_than = 100
        cheat_count_max = 20
        
    frmt = "{:>02} "*len(grid[0])    
    print("  " + frmt.format(*[str(i) for i in range(len(grid[0]))]))
    frmt = "{:>2} "*len(grid[0])  
    for idx,line in enumerate(grid):        
        print("%(number)02d" % {"number":idx} + frmt.format(*line) )
    
    start,end = start_end_find(grid)
    print(f"Start: {start}\tEnd: {end}")
    distances = dijkstra(grid,start,end,0)
    nocheat_time = distances[end][0]
    path_nocheat = []
    spot = end
    while(spot != distances[spot][1]):
        path_nocheat.append(spot)
        spot = distances[spot][1]
    path_nocheat.append(spot)
    path_nocheat.reverse()
    # print(path_nocheat)
    
    # they state only 1 path is possible for completion
    # thus cheat start and end point must be on track
    # determine the 1 path, then ensure manhattan distance between cheat start and end point < cheat count
    # determine time won from cheat count with original dijkstra
    cheat_times = {}
    for idx_start, cheat_start in enumerate(path_nocheat):
        for idx_end, cheat_end in enumerate(path_nocheat):
            diff = manhattan_distance(cheat_start,cheat_end)
            if(diff < abs(idx_end-idx_start)) and (diff <= cheat_count_max):
                cheat_time = diff + distances[cheat_start][0] + (nocheat_time - distances[cheat_end][0])
                cheat_time_diff = nocheat_time - cheat_time
                if(cheat_time_diff >= faster_than):
                    if(cheat_time_diff not in cheat_times):
                        cheat_times[cheat_time_diff] = 1
                    else:
                        cheat_times[cheat_time_diff] += 1
    
    keys_list = list(cheat_times.keys())
    keys_list.sort()
    
    total_cheats_count = 0
    for key in keys_list:
        # if(key > faster_than):
        total_cheats_count += cheat_times[key]
        print(f"There are {cheat_times[key]} cheats that save {key} picoseconds ")
    print("===================================================================================")
    print(f"There are {total_cheats_count} cheats that save at least {faster_than} picoseconds")
    