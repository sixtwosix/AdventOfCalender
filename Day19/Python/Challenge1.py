def parse_file(fileName : str) -> tuple[list[str],list[str]]:
    with open(fileName, 'r') as f:
        lines = f.readlines()
        pattern_list = lines[0].split(", ")
        pattern_list = list(map(str.strip,pattern_list))
        pattern_match = lines[2:]
        pattern_match = list(map(str.strip,pattern_match))
    
    return (pattern_list,pattern_match)

def can_make_pattern(avail_pat: list[str], match_pat: str, cache: dict) -> bool:
    
    if(match_pat in cache):
        return cache[match_pat]
    
    if(match_pat == ""):
        return True
    for idx, pat in enumerate(avail_pat):        
        if(match_pat.startswith(pat)):
            remain_pat = match_pat[len(pat):]
            if (can_make_pattern(avail_pat,remain_pat,cache)):
                cache[match_pat] = True
                return True
    
    cache[match_pat] = False
    return False
    

if __name__ == "__main__":
    fileName = "input1.csv"
    
    avail_pat, match_pat = parse_file(fileName)
    avail_pat.sort(key=len,reverse=True)
    
    if (fileName.startswith("test")):
        # test case
        print
    else:
        # normal case
        print
        
    cache = {}
    match_count = [0 for x in range(len(match_pat))]
    for idx, pat in enumerate(match_pat):
        if(can_make_pattern(avail_pat,pat,cache)):
            match_count[idx] = 1
    
    print(f"Total of {sum(match_count)} towels can be made")
    
        
    