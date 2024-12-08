# imports

def check_item_move(levels, fault_count):
    
    prev_level = False
    safe = True
    increasing = False
    decreasing = False
    
    for i in range(len(levels)):
        level = levels[i]
        if prev_level != False:
            if (level > prev_level):
                increasing = True                
                if level > (prev_level + 3):
                    safe = False
                    fault_count += 1
                
                    copy_levels = levels.copy()
                    copy_levels.pop(i)    
                    return check_item_move(copy_levels, fault_count)
                
            if (level < prev_level):
                decreasing = True
                if level < (prev_level - 3):
                    safe = False
                    fault_count += 1
                
                    copy_levels = levels.copy()
                    copy_levels.pop(i)    
                    return check_item_move(copy_levels, fault_count)
            
            if (level == prev_level):
                safe = False
                fault_count += 1
                
                copy_levels = levels.copy()
                copy_levels.pop(i)    
                return check_item_move(copy_levels, fault_count)

            if (increasing == True and decreasing == True):
                safe = False
                fault_count += 1
                
                copy_levels = levels.copy()
                copy_levels.pop(i)       
                return check_item_move(copy_levels, fault_count)

            
        prev_level = level
        
    if (safe == True):
        return levels, fault_count
    
        


if __name__ == "__main__":
    input_file = "input1.csv"
    
    with open(input_file, 'r') as f:
        
        lines = f.readlines()
    count = 0
    
    for levels in lines:
        levels = list(map(int,levels.strip().split(" ")))
        fault_count = 0
        levels, fault_count = check_item_move(levels, fault_count)
        if(fault_count <= 1):
            count += 1
            print(f"{levels} -- {fault_count}")
            
    
    print(f"Safe count: {count}")
            
            