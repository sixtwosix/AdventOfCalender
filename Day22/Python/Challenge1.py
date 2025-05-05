import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(2500)
print(sys.getrecursionlimit())

def parse_file(fileName: str) -> list[int]:
    with open(fileName,'r') as f:
        init_secret_nums = f.readlines()
        init_secret_nums = list(map(lambda x: int(x.strip()),init_secret_nums))
    
    return init_secret_nums

def get_secret_num_to_depth(init_secret_num: int, maximum_depth_level: int, cache: dict):
    
    def determine_secret_num(secret_num: int, depth_level: int):
        
        if((secret_num,depth_level) in cache):
            return cache[(secret_num,depth_level)]
        
        if(depth_level == maximum_depth_level):
            n =  secret_num            
        else:
            new_secret_num = secret_num
            n = secret_num
            # multiply by 64, mix result, prune secret
            n = n * 64
            n ^= new_secret_num
            n = n % 16777216
            new_secret_num = n
            
            # divide by 32 to nearest int, mix result, prune secret
            n = n // 32
            n ^= new_secret_num
            n = n % 16777216
            new_secret_num = n
            
            # multiply by 2048, mix result, prune secret
            n = n * 2048
            n ^= new_secret_num
            n = n % 16777216 
            new_secret_num = n
            
            n = determine_secret_num(new_secret_num, depth_level + 1)
        
        cache[(secret_num,depth_level)] = n
        return n
    
    return determine_secret_num(init_secret_num, 0),cache
            

if __name__ == "__main__":
    fileName = "input1.csv"
    init_secrets = parse_file(fileName)
    print(init_secrets)
    
    total = 0
    for secret in init_secrets:
        res, cached = get_secret_num_to_depth(secret,2000,{})
        print(f"{secret}:\t{res}")
        total += res
    print(f"Sum of secret numbers:\t{total}")