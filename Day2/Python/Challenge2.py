## Inputs -------------------------------------------------------------------------
input_file = "./test_input.csv"

## Functions ----------------------------------------------------------------------
def checkLevelsSafety(list_levels,problem_count,var_safe):
    list_levels_safe = []
    list_diff = []
    for i in range(len(list_levels)-1):
        list_diff.append(list_levels[i+1]-list_levels[i])
        # if(abs(list_levels[i+1] - list_levels[i]) >= 1) and (abs(list_levels[i+1] - list_levels[i]) <= 3):            
        #     if(list_levels[i+1] > list_levels[i]):
        #         temp_safe = 1
        #     else:
        #         temp_safe = -1
            
        #     list_levels_safe.append(temp_safe)
            
        #     # if(var_safe == None):
        #     #     var_safe = temp_safe
        #     # elif(temp_safe == 1) and (var_safe == 1):
        #     #     continue
        #     # elif(temp_safe == -1) and (var_safe == -1):
        #     #     continue
        #     # else:                
        #     #     problem_count += 1
        #     #     var_safe = 0
        #     #     list_levels.pop(i)
        #     #     return list_levels,problem_count,var_safe
        # else:            
        #     # problem_count += 1
        #     # var_safe = 0
        #     # list_levels.pop(i)
        #     # return list_levels,problem_count,var_safe
        #     list_levels_safe.append(0)
    print(list_diff)
    
    # direction = 0
    # for i in range(len(list_diff)):
        
        
    # return list_levels,problem_count,var_safe

## Main ---------------------------------------------------------------------------

with open(input_file,'r') as f:
    lines = f.readlines()
    list_safe = [ None for x in range(len(lines))]
    for x in range(len(lines)):
        line = lines[x].strip()
        list_levels = list(map(int, line.split(",")))
        problem_count = 0
        checkLevelsSafety(list_levels,problem_count,list_safe[x])
        # list_levels,problem_count,temp_safe = checkLevelsSafety(list_levels,problem_count,list_safe[x])
        # if(problem_count == 1):
        #     list_levels,problem_count,temp_safe = checkLevelsSafety(list_levels,problem_count,list_safe[x])
        # list_safe[x] = temp_safe
    
    print(list_safe)
    print(len(list_safe) - list_safe.count(0))
                    
