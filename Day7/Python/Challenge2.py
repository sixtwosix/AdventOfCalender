import numpy as np

def add_nums(x,y):
    return x + y

def multiply_nums(x,y):
    return x * y

def concat_nums(x,y):
    return int(str(x)+str(y))

def zero_padded_base_x(x,N,WIDTH):
    res = np.base_repr(x,3)
    res = '0' * (WIDTH - len(res)) + res
    return res
    

if __name__ == "__main__":
    input_file = "input1.csv"
    
    all_text = []
    
    with open(input_file,'r') as f:
        all_text = f.readlines()
    
    big_total = 0
    x_count = 0
    
    for line in all_text:
        x_count += 1
        print(x_count)
        
        final_val = int(line.split(":")[0])
        remaining_vals = line.split(":")[1].split(" ")[1:]
        remaining_vals = list(map(str.strip,remaining_vals))
        remaining_vals = list(map(int,remaining_vals))
        operators = [0 for i in range(len(remaining_vals)-1)]        
        # print(f"Final Val = {final_val}\nRemaining Vals = {remaining_vals}\nOperators = {operators}")        
        
        for x in range(pow(3,len(operators))):
            # print(format(x,f'0{str(len(operators))}b'))
            temp_operators_list = list(map(int,zero_padded_base_x(x,3,len(operators))))            
            # print(temp_operators_list)
            # temp_operators_list = list(map(int,list(format(x,f'0{str(len(operators))}b'))))
            temp_total = remaining_vals[0]
            for i in range(len(temp_operators_list)):
                match temp_operators_list[i]:
                    case 0:
                        temp_total += remaining_vals[i+1]
                    case 1:
                        temp_total *= remaining_vals[i+1]
                    case 2:
                        temp_total = concat_nums(temp_total,remaining_vals[i+1])
            
            if (temp_total == final_val):
                # print(temp_total)
                big_total += temp_total
                break
    
    print(f"Final value: {big_total}")