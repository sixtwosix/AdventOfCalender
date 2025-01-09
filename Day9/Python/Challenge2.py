import copy
from tqdm import tqdm

def rindex(lst,value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

if __name__ == "__main__":
    input_file = "input1.csv"

    with open(input_file, 'r') as f:
        disk_map = f.readlines()[0]
    
    data_block = []
    block_count = 0
    for i in range(len(disk_map)):        
        block_size = int(disk_map[i])
        if(i%2 == 0):
            new_block = [block_count, block_size]
            block_count += 1    
        else:
            new_block = ['.', block_size]
        data_block.append(new_block)
    
    # print(data_block)
    
    block_numbers = list(filter(lambda x: x[0] != '.', copy.deepcopy(data_block)))
    # print(block_numbers)
    print("shuffling blocks")
    for j in tqdm(range(len(block_numbers))):
    # for block_num in block_numbers[::-1]:
        block_num = block_numbers[::-1][j]
        for i in range(len(data_block)):
            block = data_block[i]
            if(block[0] != '.'):
                continue
            if(block_num[1] <= block[1]):                
                index = data_block.index(block_num)
                if(i > index):
                    break
                data_block[index][0] = '.'
                new_size = block[1]-block_num[1]                
                data_block[i] = block_num
                if(new_size > 0):
                    new_block = ['.',new_size]
                    data_block.insert(i+1,new_block)
                # print(data_block)
                break
    print("calculating totals")
    total = 0
    count = 0
    for block in data_block:
        for x in range(block[1]):
            if(block[0] != '.'):
                total+=block[0]*count
            count+=1
    
    print(total)
        
    
                
                    
                
                
                