# imports

# matching constants
MATCH_NORMAL = ["M","A","S"]
MATCH_REVERSED = ["S","A","M"]

# look diagonally
def check_x_mas(x,y,list_all):
    # print("Checking diagonally")
    match_coordinates = []
    list_possible = []
    if(y + 3) <= Y_MAX_VAL and (x + 3) <= X_MAX_VAL:
        list_possible = [list_all[y+a][x+a] for a in range(3)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i,y+i) for i in range(3)])
            
    if(y - 3) >= 0 and (x - 3) >= 0 :
        list_possible = [list_all[y-a][x-a] for a in range(3)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x-i,y-i) for i in range(3)])
    
    if(y + 3) <= Y_MAX_VAL and (x - 3) >= 0:
        list_possible = [list_all[y+a][x-a] for a in range(3)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x-i,y+i) for i in range(3)])
    
    if(y - 3) >= 0 and (x + 3) <= X_MAX_VAL:
        list_possible = [list_all[y-a][x+a] for a in range(3)]
        if(list_possible == MATCH_NORMAL) or (list_possible == MATCH_REVERSED):
            match_coordinates.append([(x+i,y-i) for i in range(3)])
    
    return match_coordinates            
            
def add_result(val, matches_count, list_results_cords, mock_data):   
    if(val not in list_results_cords) and (val[::-1] not in list_results_cords):
        str_text = [list_all[i[1]][i[0]] for i in val]
        # print(f"{matches_count}:\t{val} \t {str_text}")
        matches_count += 1
        list_results_cords.append(val)
        
        for i in val:
            mock_data[i[1]][i[0]] = list_all[i[1]][i[0]]
        
    return matches_count,list_results_cords, mock_data
    
    
if __name__ == "__main__":
    input_file = "./input2.csv"
    output_file = "./output2.csv"
    list_all = []
    list_all
    list_results_cords = [] 

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

    # search for letter "S" or "M" the only ones where it can start or end
    for y in range(len(list_all)):
        for x in range(len(list_all[y])):
            if(list_all[y][x] == "S") or (list_all[y][x] == "M"):
                res = check_x_mas(x,y,list_all)
                if(res != []):
                    for val in res:
                        matches_count,list_results_cords,mock_data = add_result(val,matches_count,list_results_cords, mock_data)
    
    with open(output_file,'w') as f: 
        for mock_row in mock_data:
            line = ''.join(mock_row)
            f.write(line + "\n")
    
    list_x_mas_results = []
    
    for i in range(len(list_results_cords)):
        
        copy_list_results_cords = list_results_cords.copy()
        copy_list_results_cords.pop(i)
        
        for copy_res in copy_list_results_cords:
            if(list_results_cords[i][1] == copy_res[1]):
                if([list_results_cords[i],[copy_res]] not in list_x_mas_results) and ([[copy_res],[list_results_cords[i]]] not in list_x_mas_results):
                    list_x_mas_results.append([list_results_cords[i],[copy_res]])
    
    print(len(list_x_mas_results))
    # for res in list_x_mas_results:
    #     print(res)
    


