

def rindex(lst,value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

if __name__ == "__main__":
    input_file = "input1.csv"


    with open(input_file, 'r') as f:
        disk_map = f.readlines()[0]
    
    file_blocks = []
    file_blocks_non_empty = []
    block_count = 0

    for i in range(len(disk_map)):
        block_size = int(disk_map[i])
        if(i%2 == 0):
            file_blocks += [block_count for x in range(block_size)]
            file_blocks_non_empty += [block_count for x in range(block_size)]
            block_count += 1
        else:
            file_blocks += ['.' for x in range(block_size)]
    
    file_blocks = list(map(str,file_blocks))
    file_blocks_non_empty = list(map(str,file_blocks_non_empty))

    # print(''.join(file_blocks))
    # print(''.join(file_blocks_non_empty))

    temp_str = ''
    for i in range(len(file_blocks)):
        if(file_blocks[i] == '.'):
            if not (len(file_blocks_non_empty) > 0):
                break
            temp_str = file_blocks_non_empty.pop()
            index = rindex(file_blocks,temp_str)
            file_blocks[index] = '.'
            file_blocks[i] = temp_str
        else:
            index = file_blocks_non_empty.index(file_blocks[i])
            file_blocks_non_empty.pop(index)
    
    file_blocks_compacted_non_empty = list(filter(lambda x: x != '.',file_blocks))

    # print(''.join(file_blocks))
    # print(''.join(file_blocks_compacted_non_empty))

    file_blocks_compacted_non_empty = list(map(int,file_blocks_compacted_non_empty))

    total = 0

    for i in range(len(file_blocks_compacted_non_empty)):
        total += (i * file_blocks_compacted_non_empty[i])
    
    print(f"Final checksum value: {total}")

    