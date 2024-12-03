input_file = "./input1.csv"

with open(input_file,'r') as f:
    lines = f.readlines()
    list_safe = [ None for x in range(len(lines))]
    for x in range(len(lines)):
        line = lines[x].strip()
        list_levels = list(map(int, line.split(",")))
        for i in range(len(list_levels)-1):
            if(abs(list_levels[i+1] - list_levels[i]) >= 1) and (abs(list_levels[i+1] - list_levels[i]) <= 3):            
                if(list_levels[i+1] > list_levels[i]):
                    temp_safe = 1
                else:
                    temp_safe = -1
                
                if(list_safe[x] == None):
                    list_safe[x] = temp_safe
                elif(temp_safe == 1) and (list_safe[x] == 1):
                    continue
                elif(temp_safe == -1) and (list_safe[x] == -1):
                    continue
                else:
                    list_safe[x] = 0
                    break
            else:
                list_safe[x] = 0
                break
    
    print(list_safe)
    print(len(list_safe) - list_safe.count(0))
                    
       