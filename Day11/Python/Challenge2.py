from tqdm import tqdm
import time
import itertools
from functools import cache

def rule_one(val):    
    return 1

def rule_two(val):    
    x_str = str(val)
    x1 = int(x_str[:round(len(x_str)/2)])
    x2 = int(x_str[round(len(x_str)/2):])    
    return [x1,x2]
    
def rule_three(val):
    x = int(val)*2024
    return x

# function fails, takes up to much memory
def all_rules(val, depth, dict_map, final_vals):    
    
    if(val in dict_map):
        res = dict_map[val]
    elif(int(val) == 0):
        res = [rule_one(val)]
    elif(len(str(val))%2 == 0):
        x1, x2 = rule_two(val)
        res = [x1,x2]
    else:
        res = [rule_three(val)]
    
    dict_map[val] = res
    
    if(depth == 0):
        # print(res)
        for final_val in res:
            final_vals.append(final_val)
        return res
    else:
        new_res = []
        for val in res:
            new_res.append(all_rules(val,depth-1,dict_map,final_vals))
        res = new_res
        
    return res

# create dictionary to reference how many stones will still be create depending on depth and stone value
# dictionary value consists of how much it will split into at which depth
# dictionary key = value

def expand(val, depth, dict_map):
    if(depth == 0):
        return 1
    else:
        if((val,depth) in dict_map):
            return dict_map[(val,depth)]
        elif(val == 0):
            stone_count = expand(rule_one(val),depth-1,dict_map)
        elif(len(str(val))%2 == 0):
            x1, x2 = rule_two(val)
            stone_count = expand(x1,depth-1,dict_map) + expand(x2,depth-1,dict_map)
        else:
            stone_count = expand(rule_three(val),depth-1,dict_map)
        
        dict_map[(val,depth)] = stone_count
        return stone_count
    
if __name__ == "__main__":
    
    input_file = "input1.csv"
    
    stones = []
    
    with open(input_file, 'r') as f:
        line = f.readlines()
    
    stones = ''.join(line)
    stones = stones.strip()
    stones = stones.split(' ')    
    
    blinks = 75
    
    overall_start = time.time()
    
    dict_map = {}
    final_vals = []
    
    stones = list(map(int,stones))
    
    # stone counts per stone, how many stones will be created from each stone
    stone_counts = list(map(lambda x: expand(x,blinks,dict_map),stones))
    # print(stone_counts)
    # print(sum(stone_counts))
        
    print(f"After {blinks} blinks there will be {sum(stone_counts)} stones")
    print(f"Total time: {time.time() - overall_start}")
    