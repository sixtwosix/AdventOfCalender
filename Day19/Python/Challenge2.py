def parse_file(fileName : str) -> tuple[list[str],list[str]]:
    with open(fileName, 'r') as f:
        lines = f.readlines()
        pattern_list = lines[0].split(", ")
        pattern_list = list(map(str.strip,pattern_list))
        pattern_match = lines[2:]
        pattern_match = list(map(str.strip,pattern_match))
    
    return (pattern_list,pattern_match)

def total_ways_make_pattern(avail_pat: list[str], match_pat: str, cache: dict) -> tuple[int,dict]:
    
    if(match_pat in cache):
        return cache[match_pat], cache
    
    if(match_pat == ""):
        return 1, cache, 
    
    total_ways = 0
    for idx, pat in enumerate(avail_pat):        
        if(match_pat.startswith(pat)):
            remain_pat = match_pat[len(pat):]
            res, cache = total_ways_make_pattern(avail_pat,remain_pat,cache)
            total_ways += res
    
    cache[match_pat] = total_ways
    return total_ways, cache

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
    total = 0
    for idx, pat in enumerate(match_pat):        
        res, cache = total_ways_make_pattern(avail_pat, pat, cache)            
        total += res
    
    print(f"Number of different ways to arrange designs {total}")
    