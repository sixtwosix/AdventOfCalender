import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(2500)
# print(sys.getrecursionlimit())

def parse_file(fileName: str) -> list[int]:
    with open(fileName,'r') as f:
        init_secret_nums = f.readlines()
        init_secret_nums = list(map(lambda x: int(x.strip()),init_secret_nums))
    
    return init_secret_nums

def get_secret_num_to_depth(init_secret_num: int, maximum_depth_level: int, cache: dict):
    
    def determine_secret_num(secret_num: int, depth_level: int):
        
        if((init_secret_num,depth_level) in cache):
            return cache[(init_secret_num,depth_level)]
        
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
        
        # only worried about last digit
        cache[(init_secret_num,depth_level)] = secret_num % 10
        return n
    
    return determine_secret_num(init_secret_num, 0),cache

test_set1 = {}

def determine_stock_market(init_secrets: list[int]) -> dict:   
    SECRET_NUMBER_COUNT = 2000
    
    stock_market = {}
    stock_cost = [0 for idx in range(len(init_secrets))]
    for idx,secret in enumerate(init_secrets):
        res, cache = get_secret_num_to_depth(secret,SECRET_NUMBER_COUNT,{})
        temp_prices = [val for val in cache.values()][::-1]
        
        price_diff = []
        for i,item in enumerate(temp_prices):
            if(i == 0):
                price_diff.append((item,None))
            else:
                price_diff.append((item,item - price_diff[i-1][0]))
                if(i >= 3):
                    temp_str = tuple([price_diff[j][1] for j in range(i-3,i+1)])
                    if(temp_str not in stock_market):
                        stock_market[temp_str] = stock_cost.copy()
                    # monkey will buy the first time he sees the sequence
                    if(stock_market[temp_str][idx] == 0):
                        stock_market[temp_str][idx] = item

        test_set1[(idx)] = price_diff
    
    return stock_market


if __name__ == "__main__":
    fileName = "input1.csv"
    init_secrets = parse_file(fileName)
    
    stock_market = determine_stock_market(init_secrets)
    
    biggest_winner = 0
    winner_val = []
    best_stock = ""
    for key,val in stock_market.items():
        stock_total_cost = sum(val)
        if(stock_total_cost >= biggest_winner):
            biggest_winner = stock_total_cost
            best_stock = key
            winner_val = val
    print(f"The best combo of \"{best_stock}\"\nwill yield {biggest_winner} bananas")