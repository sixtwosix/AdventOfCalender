import re

def parse_input_file(input_file):
    with open(input_file,'r') as f:
        list_groups = f.readlines()
        list_groups.append("\n")
        regex_str = "Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
        
        list_block = []
        temp_str = ""
        for group in list_groups:
            if(group != "\n"):
                temp_str += group
            else:
                x = re.match(regex_str,temp_str)
                list_block.append([
                                    int(x.group(1)), ## btn A X - 0
                                    int(x.group(2)), ## btn A Y - 1
                                    int(x.group(3)), ## btn B X - 2
                                    int(x.group(4)), ## btn B Y - 3
                                    int(x.group(5)), ## btn Final X - 4
                                    int(x.group(6)), ## btn Final Y - 5 
                                   ])
                temp_str = ""
    
    return list_block

if __name__ == "__main__":
    
    input_file_name = "input1.csv"
    list_machines = parse_input_file(input_file_name)
    # print(list_machines)
    
    total_cost = 0
    prizes_won = 0
    
    for machine in list_machines:
        b = (machine[5]*machine[0] - machine[1]*machine[4] )/(machine[3]*machine[0] - machine[1]*machine[2])
        a = (machine[4] - b*machine[2])/(machine[0])
        if(a == int(a)) and (b == int(b)):
            # print(f"Press Btn A \"{a}\" times ----  Press Btn B \"{b}\" times")
            if((a < 100) and (b < 100)):
                total_cost += (a*3 + b*1)
                prizes_won += 1            
        # else:
        #     print("Can not reach the goal")
    
    print(f"Total cost: {total_cost}\nWin {prizes_won} prizes")
            
        
        
    