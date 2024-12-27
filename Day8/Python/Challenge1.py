import copy

def print_map(antenna_map,freq = ""):
    with open('output1.csv','a') as f:
        f.writelines(''.join([freq for z in range(len(antenna_map[0]))]) + "\n")
        for line in antenna_map:
            # print(line)            
            f.writelines(f"{''.join(line)}\n")


def find_all_antennas(antenna_map,ROW_MAX,COL_MAX):
    
    set_antennas = set()

    for row in range(ROW_MAX):
        for col in range(COL_MAX):
            if(antenna_map[row][col] != "."):
                set_antennas.add((col,row,antenna_map[row][col]))
    
    return set_antennas

def function_between_nodes(node1, node2, ROW_MAX, COL_MAX):
    set_antinodes = set()

    antenna_type = node1[2]
    a = (node1[1]-node2[1])/(node1[0]-node2[0])
    b = node1[1] - (a * node1[0])

    diff_x = abs(node1[0]-node2[0])
    x_min_antinode = min(node1[0],node2[0]) - diff_x
    x_max_antinode = max(node1[0],node2[0]) + diff_x
    if(x_min_antinode == 46 or x_max_antinode == 46):
        print
    if(0 <= x_max_antinode < COL_MAX):
        y_max_antinode = (a * (x_max_antinode)) + b
        if(0 <= y_max_antinode < ROW_MAX):
            set_antinodes.add((x_max_antinode,round(y_max_antinode),antenna_type))
    
    if(0 <= x_min_antinode < COL_MAX):
        y_min_antinode = (a * (x_min_antinode)) + b
        if(0 <= y_min_antinode < ROW_MAX):
            set_antinodes.add((x_min_antinode,round(y_min_antinode),antenna_type))
    
    return set_antinodes

def create_antinodes(antenna_map1, set_antinodes):
    
    for antinode in set_antinodes:
        if(antenna_map1[antinode[1]][antinode[0]] == "."):
            antenna_map1[antinode[1]][antinode[0]] = "#"
    
    return antenna_map1




if __name__ == "__main__":
    input_file = "input1.csv"

    with open(input_file,'r') as f:
        lines = list(f.readlines())
    
    antenna_map = list(map(str.strip,lines))
    antenna_map = list(map(list,antenna_map))

    ROW_MAX = len(antenna_map)
    COL_MAX = len(antenna_map[0])

    count_antinodes = 0
    # new_antinodes = set()

    

    # find all antennas, make a list for each individual antenna with x, y
    set_antennas = find_all_antennas(antenna_map,ROW_MAX,COL_MAX)
    # set_antenna_types = set([a[2] for a in set_antennas])
    set_antenna_types = ["G","P","a","j","z","d","Z","Y","T","u","8","l","n","x","A","q","s","3","g","Q","p","t","2","c","f","X","1","i","7","N","W","F","5","S","9","o","R","E","y","H","L","e","0","6","r","I","U","D","4","w","O","J","h","C","5"]
    # print(set_antennas)
    # print(set_antenna_types)

    antinodes = set()

    for antenna_type in set_antenna_types:
        antenna_map_new = copy.deepcopy(antenna_map)
        antenna_groups = list(filter(lambda x: x[2] == antenna_type,set_antennas))
        new_antinodes = set()
        for i in range(len(antenna_groups)):
            for j in range(len(antenna_groups)):
                if(i == j):
                    continue
                else:
                    set_antinodes = function_between_nodes(antenna_groups[i],antenna_groups[j],ROW_MAX,COL_MAX)
                    # print(f"Antinodes:\n{set_antinodes}")
                    for antinode in set_antinodes:
                        new_antinodes.add(antinode)
    
        new_antinodes = set({tuple(x[:2]): x for x in new_antinodes}.values())
        antenna_map_new = list(create_antinodes(antenna_map_new,new_antinodes))
        
        # print(new_antinodes)

        # print_map(antenna_map_new,antenna_type)
        for antinode in new_antinodes:
            antinodes.add(antinode)


    antinodes = set({tuple(x[:2]): x for x in antinodes}.values())
    count_antinodes = len(antinodes)
    print(f"Total antinodes: {count_antinodes}")

