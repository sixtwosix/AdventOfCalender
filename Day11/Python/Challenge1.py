from tqdm import tqdm
import time

def rule_one(val):    
        return ['1']

def rule_two(val):    
    x1 = int(val[:round(len(val)/2)])
    x2 = int(val[round(len(val)/2):])
    return [str(x1),str(x2)]
    
def rule_three(val):
    x = int(val)*2024
    return [str(x)]

def all_rules(val):
    if(int(val) == 0):
        return rule_one(val)
    elif(len(val)%2 == 0):
        return rule_two(val)
    else:
        return rule_three(val)

    
if __name__ == "__main__":
    
    input_file = "test_input1.csv"
    
    stones = []
    
    with open(input_file, 'r') as f:
        line = f.readlines()
    
    stones = ''.join(line)
    stones = stones.strip()
    stones = stones.split(' ')    
    
    blinks = 6
    
    overall_start = time.time()
    
    for i in tqdm(range(blinks)):        
        stones = list(map(all_rules,stones))
        stones = sum(stones, [])
        # print(stones)
        
    print(f"Stones total after {blinks} blinks: {len(stones)}")
    print(f"Total time: {time.time() - overall_start}")
    