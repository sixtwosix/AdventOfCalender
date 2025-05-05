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
        
        if((init_secret_num,depth_level) in cache):
            return cache[(init_secret_num,depth_level)]
        
        if(depth_level == maximum_depth_level-1):
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
        
        # only worried about last digit
        cache[(init_secret_num,depth_level)] = secret_num % 10
        return n
    
    return determine_secret_num(init_secret_num, 0),cache

def determine_stock_market(init_secrets: list[int]) -> list[list[tuple[int,str]]]:   
    SECRET_NUMBER_COUNT = 10
     
    stock_market = [[] for idx in range(len(init_secrets))]
    for idx,secret in enumerate(init_secrets):
        res, cache = get_secret_num_to_depth(secret,SECRET_NUMBER_COUNT,{})
        temp_prices = [val for key, val in cache.items()][::-1]
        price_diff = []
        possible_choices = []
        for i,item in enumerate(temp_prices):
            if(i == 0):
                price_diff.append((i,item,None))
            else:
                price_diff.append((i,item,item-prev_item))
                if(i > 4):
                    temp_str = ""
                    for j in range(3,-1,-1):
                        temp_str += str(price_diff[i-j][2])
                    possible_choices.append((item,temp_str))
            
            prev_item = item

        
        possible_choices = sorted(possible_choices, key=lambda x: (x[0], x[1]), reverse=True)
        # for item_x in possible_choices:
        #     print(item_x)
        stock_market[idx] = possible_choices
    
    return stock_market
    
def play_stock_market():
    print()            

if __name__ == "__main__":
    fileName = "test_input3.csv"
    init_secrets = parse_file(fileName)
    print(init_secrets)
    
    stock_market = determine_stock_market(init_secrets)
    
    for i in range(len(stock_market[0])):
        print(f"{stock_market[0][i]}\t{stock_market[1][i]}\t{stock_market[2][i]}\t{stock_market[3][i]}")