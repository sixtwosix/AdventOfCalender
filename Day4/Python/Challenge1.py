# imports

# matching constants
MATCH_NORMAL = ["X","M","A","S"]
MATCH_REVERSED = ["S","A","M","X"]

# look diagonally
def check_diagonal(x,y,list_all):
    # print("Checking diagonally")
    match_coordinates = []
    list_possible = []
    if(y + 4) <= Y_MAX_VAL and (x + 4) <= X_MAX_VAL:
        list_possible = [list_all[y+a][x+a] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i,y+i) for i in range(4)])
            
    if(y - 4) >= 0 and (x - 4) >= 0 :
        list_possible = [list_all[y-a][x-a] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x-i,y-i) for i in range(4)])
    
    if(y + 4) <= Y_MAX_VAL and (x - 4) >= 0:
        list_possible = [list_all[y+a][x-a] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x-i,y+i) for i in range(4)])
    
    if(y - 4) >= 0 and (x + 4) <= X_MAX_VAL:
        list_possible = [list_all[y-a][x+a] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i,y-i) for i in range(4)])
    
    return match_coordinates
# look vertically
def check_vertical(x,y,list_all):
    # print("Checking vertically")
    match_coordinates = []
    list_possible = []
    if(y + 4) <= Y_MAX_VAL:
        list_possible = [list_all[y+a][x] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x,y+i) for i in range(4)])
    if(y - 4) >= 0 :
        list_possible = [list_all[y-4+a][x] for a in range(4)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x,y+i-4) for i in range(4)])
    return match_coordinates

# look horizontally
def check_horizontal(x,y,list_all):
    # print("Checking horizontally")
    match_coordinates = []
    list_possible = []
    if(x + 4) <= X_MAX_VAL:
        list_possible = list_all[y][x:x+4]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i,y) for i in range(4)])
    if(x - 4) >= 0 :
        list_possible = list_all[y][x-4:x]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i-4,y) for i in range(4)])
    return match_coordinates
            
            
def add_result(val, matches_count, list_results_cords, mock_data):   
    if(val not in list_results_cords.values()) and (val[::-1] not in list_results_cords.values()):
        str_text = [list_all[i[1]][i[0]] for i in val]
        # print(f"{matches_count}:\t{val} \t {str_text}")
        matches_count += 1
        list_results_cords[matches_count] = val
        
        for i in val:
            mock_data[i[1]][i[0]] = list_all[i[1]][i[0]]
        
    return matches_count,list_results_cords, mock_data
    
    
if __name__ == "__main__":
    input_file = "./input1.csv"
    output_file = "./output1.csv"
    list_all = []
    list_all
    list_results_cords = {} #Key = count -- Value = [x,y] cords

    # read file into array
    with open(input_file,'r') as f:
        list_all = f.readlines()

    for i in range(len(list_all)):
        list_all[i] = list(list_all[i].strip())
        
    X_MAX_VAL = len(list_all )
    Y_MAX_VAL = len(list_all[0])
    
    mock_data = [["." for i in range(X_MAX_VAL)] for j in range(Y_MAX_VAL)]
    
    # print(f"Max Y: {Y_MAX_VAL}\tMax X: {X_MAX_VAL}")        
    # for row in list_all:
    #     print(row)
    
    matches_count = 0

    # search for letter "S" or "X" the only ones where it can start or end
    for y in range(len(list_all)):
        for x in range(len(list_all[y])):
            if(list_all[y][x] == "X") or (list_all[y][x] == "S"):
            # if(list_all[y][x] == "X"):
                res = check_horizontal(x,y,list_all)
                if(res != []):
                    for val in res:
                        matches_count,list_results_cords,mock_data = add_result(val,matches_count,list_results_cords, mock_data)
                res = check_vertical(x,y,list_all)
                if(res != []):
                    for val in res:
                        matches_count,list_results_cords,mock_data = add_result(val,matches_count,list_results_cords, mock_data)
                res = check_diagonal(x,y,list_all)
                if(res != []):
                    for val in res:
                        matches_count,list_results_cords,mock_data = add_result(val,matches_count,list_results_cords, mock_data)
    
    with open(output_file,'w') as f: 
        for mock_row in mock_data:
            line = ''.join(mock_row)
            f.write(line + "\n")
    
    print(f"Number of matches: {len(list_results_cords)}")


