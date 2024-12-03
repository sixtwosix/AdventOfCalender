import re
import numpy as np

input_file = "./test_input2.txt"

with open(input_file, 'r') as f:
    text = f.read()
    
    all_mul = re.findall(r"(do(?:n't){0,1}\(\))|mul\(([0-9]{1,3})\,([0-9]{1,3})\)", text)
    
    total = 0
    can_mul = True
    
    for item in all_mul:
        if(item[0] == '') and (can_mul):            
            item = tuple(map(int, item[1:]))
            print(f"Multiply these {str(item)}")
            mul = np.prod(item)
            print(f"to get this {mul}")
            total += mul
        elif(item[0] == "don't()"):
            can_mul = False
        elif(item[0] == "do()"):
            can_mul = True
            
    
    print(f"Total: {total}")