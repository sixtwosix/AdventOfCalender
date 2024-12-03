## Imports -------------------------------------------------------------------------


## Functions ----------------------------------------------------------------------

def increasingCheck(list_data):
    return [0 if (x < y) else 1 for x,y in zip(list_data,list_data[1:])]

def decreasingCheck(list_data):
    return [0 if (x > y) else 1 for x,y in zip(list_data,list_data[1:])]

def stepCheck(list_data):
    return [0 if (abs(x - y) < 4) else 1 for x,y in zip(list_data,list_data[1:])]    

# TODO: Write recursive function that continously removes first fault and keeps fault counter
def checkSafety(list_data, fault_count):
    # print(f"\nList: {list_data} \t Fault count: {fault_count}")
    list_increaseCheck = increasingCheck(list_data)    
    list_decreaseCheck = decreasingCheck(list_data)
    list_stepCheck = stepCheck(list_data)
    
    sum_increaseCheck = sum(list_increaseCheck)
    sum_decreaseCheck = sum(list_decreaseCheck)
    sum_stepCheck = sum(list_stepCheck)
    
    if(sum_increaseCheck > sum_decreaseCheck) and (sum_decreaseCheck > 0):        
        if(list_data[-1] > list_data[-2]):
            list_data.pop(-1)    
        else:
            list_data.pop(list_decreaseCheck.index(1))
        fault_count += 1
        return checkSafety(list_data, fault_count)
        
    elif(sum_decreaseCheck > sum_increaseCheck)  and (sum_increaseCheck > 0):
        if(list_data[-1] < list_data[-2]):
            list_data.pop(-1)    
        else:
            list_data.pop(list_increaseCheck.index(1))
        fault_count += 1
        return checkSafety(list_data, fault_count)
    
    elif(sum_stepCheck > 0) and ((sum_decreaseCheck == 0) or (sum_increaseCheck == 0)):
        x = abs(list_data[-1] - list_data[-2])
        if(x > 3) and (x < 1):
            list_data.pop(-1)    
        else:
            list_data.pop(list_stepCheck.index(1))
        fault_count += 1
        return checkSafety(list_data, fault_count)
    
    else:
        return list_data, fault_count

## Main ---------------------------------------------------------------------------
if (__name__ == "__main__"):
    input_file = "./input1.csv"
    output_file_unsafe = "./out_unsafe1.csv"
    output_file_safe = "./out_safe1.csv"
    with open(input_file,'r') as f:
        with open(output_file_unsafe, 'w') as g:
            with open(output_file_safe, 'w') as h:
                lines = f.readlines()
                
                list_safe = []
                
                for line in lines:
                    out_str = line.strip()
                    line = list(map(int,line.strip().split()))
                    list_data, fault_count = checkSafety(line, 0)
                    # print(list_data, fault_count)
                    if(fault_count > 1):
                        list_safe.append(0)
                        out_str += "\t\t X"
                        g.write(out_str + "\n")
                    else:
                        list_safe.append(1)
                        out_str += "\t\t O"
                        h.write(out_str + "\n")
                    
                    
                
        
        print(f"Total safe lists: {sum(list_safe)}")

        