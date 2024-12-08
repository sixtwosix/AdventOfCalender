# imports
    
def check_before(page_produce,expected_after,i):
    for val in expected_after:
        if(val in page_produce[0:i]):
            return True, val
    
    return False, None

def recurse_check(page_produce):
    for i in range(len(page_produce)):            
        if(page_produce[i] in page_ordering_rules):
            expected_after = page_ordering_rules[page_produce[i]]
            
            bool_before, error_page = check_before(page_produce,expected_after,i)
            if(bool_before):
                pages_good = False                    
                new_pages_produce = page_produce.copy()
                new_pages_produce.pop(new_pages_produce.index(error_page))
                # new_pages_produce.insert(i+1,error_page)
                new_pages_produce.append(error_page)
                return recurse_check(new_pages_produce)
    
    return page_produce
    
            

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
        
    # print(page_ordering_rules)
    
    pages_list_good = []
    total = 0
    for page_produce in pages_to_produce:
        # print(page_produce)
        pages_good = True
        
        corrected_pages = recurse_check(page_produce)
        
        # move around so that it is correct
        if(page_produce != corrected_pages):
            # print(f"{page_produce} -- {corrected_pages}")
            total += int(corrected_pages[int((len(corrected_pages)+1)/2)-1])
    
    print(f"Total: {total}")
        
        
    
    