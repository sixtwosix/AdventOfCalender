def parse_file(fileName: str):
    with open(fileName, 'r') as f:
        codes = f.readlines()
    
    codes = list(map(lambda x : x.strip(),codes))
    return codes

def create_grid_dictionary(keypad_dirs : dict, input_pad: dict, deadzone: tuple):
    # creates a dictionary with all the possible inputs and directional button presses to move from pad1 to pad2    
    for pad1, loc1 in input_pad.items():
        for pad2, loc2 in input_pad.items():
            pad_pair = (pad1,pad2)
            # if locations on the same x
            if (loc1[0] == loc2[0]):
                # move down to loc2
                if(loc1[1] < loc2[1]):
                    keypad_dirs[pad_pair] = "v" * abs(loc1[1] - loc2[1])
                # move up to loc2
                else:
                    keypad_dirs[pad_pair] = "^" * abs(loc1[1] - loc2[1])
            # if locations on the same y
            elif(loc1[1] == loc2[1]):
                # move right to loc2
                if(loc1[0] < loc2[0]):
                    keypad_dirs[pad_pair] = ">" * abs(loc1[0] - loc2[0])
                # move left to loc2
                else:
                    keypad_dirs[pad_pair] = "<" * abs(loc1[0] - loc2[0])
            else:
                # if loc1 x on same level as deadzone x and loc2 y on same level as deadzone y
                if(loc1[0] == deadzone[0] and loc2[1] == deadzone[1]):
                    if(loc1[1] > deadzone[1] and loc2[0] > deadzone[0]):
                        keypad_dirs[pad_pair] = '>' * abs(loc1[0] - loc2[0]) + '^' * abs(loc1[1] - loc2[1])
                    elif(loc1[1] < deadzone[1] and loc2[0] > deadzone[0]):
                        keypad_dirs[pad_pair] = '>' * abs(loc1[0] - loc2[0]) + 'v' * abs(loc1[1] - loc2[1])
                # if loc1 y on same level as deadzone y and loc2 x on same level as deadzone x
                elif(loc1[1] == deadzone[1] and loc2[0] == deadzone[0]):
                    if(loc1[0] > deadzone[0] and loc2[1] > deadzone[1]):
                        keypad_dirs[pad_pair] = 'v' * abs(loc1[1] - loc2[1]) + '<' * abs(loc1[0] - loc2[0])
                    elif(loc1[0] > deadzone[0] and loc2[1] < deadzone[1]):
                        keypad_dirs[pad_pair] = '^' * abs(loc1[1] - loc2[1]) + '<' * abs(loc1[0] - loc2[0])
                        
                else:
                    if(loc1[1] < loc2[1]):
                        vert = "v" * abs(loc1[1] - loc2[1])
                    else:
                        vert = "^" * abs(loc1[1] - loc2[1])
                    if(loc1[0] < loc2[0]):
                        horizon = ">" * abs(loc1[0] - loc2[0])
                    else:
                        horizon = "<" * abs(loc1[0] - loc2[0])
                    keypad_dirs[pad_pair] = [horizon,vert]
    return keypad_dirs

def calculate_sequence_count(init_code:str, max_depth_level: int, keypad_dir_grid: dict, known_sequences: dict):
    def and_another_one(new_sequence, depth_level):
        if(new_sequence, depth_level) in known_sequences:
            return known_sequences[(new_sequence, depth_level)]
        if depth_level == max_depth_level:
            n = len(new_sequence)
            # n = new_sequence
        else:
            n = 0
            # n = ""
            for i, next_key in enumerate(new_sequence):
                if i == 0:
                    prev_key = 'A'
                else:
                    prev_key = new_sequence[i - 1]
                sequences = keypad_dir_grid[(prev_key,next_key)]
                
                # if sequences is two different ways
                if(isinstance(sequences,list)):
                    res1 = and_another_one(sequences[0] + sequences[1] + 'A', depth_level + 1)
                    res2 = and_another_one(sequences[1] + sequences[0] + 'A', depth_level + 1)
                    n += min(res1, res2)
                    # if(len(res1) <= len(res2)):
                    #     n += res1
                    # else:
                    #     n += res2
                # only one way to move
                else:
                    n += and_another_one(sequences + 'A', depth_level + 1)
        known_sequences[(new_sequence, depth_level)] = n
        return n

    return and_another_one(init_code,0), known_sequences     

if __name__ == "__main__":
    fileName = "input1.csv"
    
    codes = parse_file(fileName)
    print(codes)
    
    numpad = { "7" : (0,0), "8" : (1,0), "9" : (2,0), "4" : (0,1), "5" : (1,1), "6" : (2,1), "1" : (0,2), "2" : (1,2), "3" : (2,2), "0" : (1,3), "A" : (2,3) }
    dirpad = { "^" : (1,0), "A" : (2,0), "<" : (0,1), "v" : (1,1), ">" : (2,1), }
    
    keypad_dir_grid = create_grid_dictionary({},numpad,(0,3))
    keypad_dir_grid = create_grid_dictionary(keypad_dir_grid,dirpad,(0,0))
    
    known_sequences = {}
    total = 0
    for code in codes:    
        res, known_sequences = calculate_sequence_count(code,3,keypad_dir_grid,known_sequences)
        # length = len(res)
        length = res
        cost = int(code[:-1]) * length        
        print(f"{code}:\t{length}\t{res}")
        total += cost
    
    print(f"Total:\t{total}")