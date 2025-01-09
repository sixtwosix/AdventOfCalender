import copy
from tqdm import tqdm

def rindex(lst,value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

if __name__ == "__main__":
    input_file = "test_input1.csv"


    with open(input_file, 'r') as f:
        disk_map = f.readlines()[0]
    
    file_blocks = []
    file_blocks_non_empty = []
    block_count = 0

    # for i in range(len(disk_map)):
    #     block_size = int(disk_map[i])
    #     if(i%2 == 0):
    #         file_blocks += [block_count for x in range(block_size)]
    #         file_blocks_non_empty += [block_count for x in range(block_size)]
    #         block_count += 1
    #     else:
    #         file_blocks += ['.' for x in range(block_size)]
    
    
    # print(file_blocks)
    # # file_blocks = list(map(str,file_blocks))
    # # file_blocks_non_empty = list(map(str,file_blocks_non_empty))

    # # print(''.join(file_blocks))
    # # print(''.join(file_blocks_non_empty))

    # values = set(map(lambda x:x, file_blocks))
    # group_vals = [[y for y in file_blocks if y!='.' and y==x ] for x in values]
    # print(group_vals)
    
    # edited_blocks = copy.deepcopy(file_blocks)
    
    # new_blocks = []
    # prev_x = ''
    # temp_list = []
    # # temp_list.append(file_blocks[0])
    # prev_x = file_blocks[0]
    # for x in file_blocks:        
    #     if(x == prev_x):
    #         temp_list.append(x)
    #     elif(len(temp_list) > 0):
    #         # temp_list.append(prev_x)
    #         new_blocks.append(temp_list)
    #         temp_list = []
    #         temp_list.append(x)
            
    #     prev_x = x
    # new_blocks.append(temp_list)
    
    # print(new_blocks)
    
    # block_numbers = list(filter(lambda x: x[0] != '.', new_blocks))
    # print(block_numbers)
    # block_spaces = list(filter(lambda x: x[0] == '.', new_blocks))
    # print(block_spaces)
    
    # for block in block_numbers[::-1]:
    #     for blank_block in block_spaces:
    #         if(len(block) <= len(blank_block)):
    
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
        
    
                
                    
                
                
                