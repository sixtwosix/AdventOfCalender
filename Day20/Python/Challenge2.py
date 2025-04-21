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
    
    heapq.heappush(pq,(start_weight,x,y,0))
    distance[(start[0],start[1],0)] = start_weight
    
    # if not (cheat_count):
    #     sys.stdout.write("\r checking cheat at (%3d,%3d)" % (start[0], start[1]))
    #     sys.stdout.flush()
    #     # print(len(pq),end='',flush=True)
    
    while pq:
        
        (weight, x ,y, cheat_count) = heapq.heappop(pq)
        
        # if((x,y) == end):
        #     return distance
        
        if(distance[(x,y,cheat_count)] < weight):
            continue
        
        for i in range(4):
            # normal section
            dx,dy = delta[i]
            new_x = x + dx
            new_y = y + dy
            if(0 <= new_y < len(grid)) and (0 <= new_x < len(grid[0])) and (grid[new_y][new_x] != "#"):
                if((new_x,new_y,cheat_count) not in distance) or (distance[(new_x,new_y,cheat_count)] > weight + 1):
                    distance[(new_x,new_y,cheat_count)] = weight + 1
                    heapq.heappush(pq,(weight+1,new_x,new_y,cheat_count))

            # cheat section
            if(cheat_count+1 <= max_cheat):
                cheat_x = x + dx
                cheat_y = y + dy
                if(0 <= new_y < len(grid)) and (0 <= new_x < len(grid[0])):                    
                    if((cheat_x,cheat_y,cheat_count+1) not in distance) or (distance[(cheat_x,cheat_y,cheat_count+1)] < weight + 1):
                        distance[(cheat_x,cheat_y,cheat_count+1)] = weight + 1
                        heapq.heappush(pq,(weight+1,cheat_x,cheat_y,cheat_count+1))
    
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

if __name__ == "__main__":
    fileName = "test_input1.csv"       
    
    grid = parse_file(fileName)
    
    if(fileName.startswith("test")):
        # test case
        faster_than = 50
    else:
        # prod case
        faster_than = 100
        
    frmt = "{:>02} "*len(grid[0])    
    print("  " + frmt.format(*[str(i) for i in range(len(grid[0]))]))
    frmt = "{:>2} "*len(grid[0])  
    for idx,line in enumerate(grid):        
        print("%(number)02d" % {"number":idx} + frmt.format(*line) )
    
    cheat_distance = {}    
    start,end = start_end_find(grid)
    print(f"Start: {start}\tEnd: {end}")
    distances = dijkstra(grid,start,end,0)
    no_cheat_time = distances[(end[0],end[1],2)]
    print()
    print(distances)
    print(f"No cheat time: {no_cheat_time}")
    # cheat_faster = {}
    # for x,y,weight_start,cheant_count in cheat_distances.keys():
    #     cheat_spot = (x,y,weight_start,cheant_count)
    #     time_diff = no_cheat_time - cheat_distances[cheat_spot]
    #     if(time_diff >= faster_than):
    #         if(time_diff in cheat_faster):
    #             cheat_faster[time_diff] += 1
    #         else:
    #             cheat_faster[time_diff] = 1
    
    # keys_list = list(cheat_faster.keys())
    # keys_list.sort()
    
    # total_cheats_count = 0
    # for key in keys_list:
    #     # if(key > faster_than):
    #     total_cheats_count += cheat_faster[key]
    #     print(f"There are {cheat_faster[key]} cheats that save {key} picoseconds ")
    # print("===================================================================================")
    # print(f"There are {total_cheats_count} cheats that save at least {faster_than} picoseconds")
    
        