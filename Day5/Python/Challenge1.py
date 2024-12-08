# imports
    
def check_before(page_produce,expected_after,i):
    for val in expected_after:
        if(val in page_produce[0:i]):
            return True
    
    return False

if __name__ == "__main__":
    
    input_file = "./input1.csv"
    
    with open(input_file, 'r') as f:
        all_data = f.readlines()
    
    page_ordering_rules = {}
    pages_to_produce = []
    first_part = True
    
    for line in all_data:
        line = line.strip()
        if(line == ''):
            first_part = False
            continue
        if(first_part):
            temp = line.split("|")
            if(temp[0] in page_ordering_rules):
                page_ordering_rules[temp[0]].append(temp[1])
            else:
                page_ordering_rules[temp[0]] = [temp[1]]
        else:
            pages_to_produce.append(line.split(","))
        
    print(page_ordering_rules)
    
    pages_list_good = []
    total = 0
    for page_produce in pages_to_produce:
        pages_good = True
        for i in range(len(page_produce)):
            
            if(page_produce[i] in page_ordering_rules):
                expected_after = page_ordering_rules[page_produce[i]]
                
                bool_before = check_before(page_produce,expected_after,i)
                if(bool_before):
                    pages_good = False
                    break
                # bool_after = check_after(page_produce,expected_after,i)
        
        pages_list_good.append(pages_good)
        
        if(not pages_good):
            continue
        
        # print(int(page_produce[int((len(page_produce)+1)/2)-1]))
        total += int(page_produce[int((len(page_produce)+1)/2)-1])
        
    print(f"Total: {total}")