

def parseInputFile(fileName : str):
    with open(fileName, 'r') as f:
        lines = f.readlines()
        temp_block = []
        keys = []
        locks = []
        
        for i,line in enumerate(lines):
            if(line != "\n") and (i != len(lines) - 1):
                temp_block.append(line.strip())           
            else:
                if(i == len(lines) - 1):
                    temp_block.append(line.strip())
                heights = determine_heights(temp_block)
                if(temp_block[0] == "#####"):
                    locks.append(heights)
                elif(temp_block[-1] == "#####"):
                    keys.append(heights)
                temp_block = []
    
    return locks,keys
                
def determine_heights(block: list):
    
    heights = [-1 for x in range(len(block[0]))]
    
    for line in block:
        for i,c in enumerate(line):
            if(c == "#"):
                heights[i] = heights[i] + 1
    
    return tuple(heights)


if __name__ == "__main__":
    fileName = "input1.csv"
    
    locks, keys = parseInputFile(fileName)
    total = 0
    
    for key in keys:
        for lock in locks:
            combo = [0 for x in range(len(key))]
            for i in range(len(key)):
                if(key[i] + lock[i] <= 5):
                    combo[i] = 5
            if(sum(combo) == len(key)*5):
                # print(f"Lock: {lock} -- Key: {key}")
                total += 1
    
    print(f"Found {total} working combinations")
    