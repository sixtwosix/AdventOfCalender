import re
import numpy as np

input_file = "./input1.txt"

with open(input_file, 'r') as f:
    text = f.read()
    
    all_mul = re.findall(r"mul\(([0-9]{1,3})\,([0-9]{1,3})\)", text)
    
    total = 0
    
    for item in all_mul:
        item = tuple(map(int, item))
        print(f"Multiply these {str(item)}")
        mul = np.prod(item)
        print(f"to get this {mul}")
        total += mul
    
    print(f"Total: {total}")