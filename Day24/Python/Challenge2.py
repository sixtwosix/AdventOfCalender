import tqdm
import re
import copy

def parsefile(fileName: str):
    with open(fileName, 'r') as f:        
        idx_cut = -1
        for i,line in enumerate(temp := f.readlines()):
            if(line == "\n"):
                idx_cut = i
                break
        wire_inputs = list(map(lambda x: x.strip().split(": "),temp[:idx_cut]))
        wire_gates = list(map(lambda x : x.strip().split(" -> "),temp[idx_cut+1:]))
    
    circuit = {}
    for input in wire_inputs:
        if(input[0][0] == "y") or (input[0][0] == "x"):
            circuit[input[0]] = input[0]
    for gate in wire_gates:
        temp = gate[0].split()
        if(temp[0][0] == "y" and temp[0][1:].isdigit()) and (temp[2][0] == "x" and temp[2][1:].isdigit()):
            gate[0] = f"x{temp[0][1:]} {temp[1]} y{temp[0][1:]}"
        circuit[gate[1]] = gate[0]
    
    return circuit

def solve_circuit(circuit: dict):
    cache = {}
    
    def determine_val(node: str):
        n = circuit[node]
        if( n[0] != -1):
            return n
        else:            
            gate = tuple(n[1].split(" "))
            if(gate in cache):
                return cache[gate]
            val1 = determine_val(gate[0])
            val2 = determine_val(gate[2])
            if(gate[1] == "AND"):
                n = f"[{val1} AND {val2}]"
            elif(gate[1] == "OR"):
                n = f"[{val1} OR {val2}]"
            elif(gate[1] == "XOR"):
                n = f"[{val1} XOR {val2}]"
        
            cache[gate] = n
            return n

    for key, val in circuit.copy().items():
        if (val[0] != "x") and (not val[1:].isdigit()) and (val[0] != "y"):
            circuit[key] = determine_val(key)            
    
    return circuit

def determine_errors(circuit: dict, memo_circuit: dict, possible_errors):
    regex_string = r"\[(\w{3}) (XOR|AND|OR) (\w{3})\]"
    circuit = {v: k for k, v in circuit.items()}
    memo_circuit = {v: k for k, v in memo_circuit.items()}
    cache = {}
    broken_wires = []
    
    def reverse_engineer(statement: str, statement_memo: str):
        if((statement,statement_memo) in cache):
            return cache[(statement,statement_memo)]
        if(statement == statement_memo):
            n = True            
        else:
            res = re.findall(regex_string,statement)
            res_memo = re.findall(regex_string,statement_memo)
            
            if(len(res) == 0 and len(res_memo) == 0):
                n = False
                broken_wires.append((statement,statement_memo))
            else:
                for x in res:
                    x1= " ".join(x)
                    x2= " ".join(x[::-1])
                    if(x1 in circuit):
                        x = x1                
                    elif(x2 in circuit):
                        x = x2
                    y = circuit[x]
                    x = f"[{x1}]"
                    statement = statement.replace(x,y)
                
                for x in res_memo:
                    x1= " ".join(x)
                    x2= " ".join(x[::-1])
                    if(x1 in circuit):
                        x = x1                
                    elif(x2 in circuit):
                        x = x2
                    else:
                        n = False
                        cache[(statement,statement_memo)] = n
                        broken_wires.append((statement,statement_memo))
                        return n
                        
                    y = circuit[x]
                    x = f"[{x1}]"
                    statement_memo = statement_memo.replace(x,y)
            
                n = reverse_engineer(statement,statement_memo)
        cache[(statement,statement_memo)] = n
        return n
    
    return reverse_engineer(f"[{possible_errors[0]}]",possible_errors[1]),broken_wires

def fix_broken_wires(circuit: str, circuit_memo: str, circuit_dict_original: dict):
    regex_string = r"\[(\w{3}) (XOR|AND|OR) (\w{3})\]"
    circuit_dict_origin = circuit_dict_original.copy()
    
    res = re.findall(regex_string,f"[{circuit}]")
    res_memo = re.findall(regex_string,circuit_memo)

    if(len(circuit) == 3 and len(circuit_memo) == 3):
        temp = circuit_dict_origin[circuit]
        temp2 = circuit_dict_origin[circuit_memo]        
        circuit_dict_origin[circuit_memo] = temp
        circuit_dict_origin[circuit] = temp2
    elif(len(res) == 0 ) and (len(res_memo) > 0):
        while(len(res) != len(res_memo)):
            circuit = circuit_dict_original[circuit]
            res = re.findall(regex_string,f"[{circuit}]")
            res_memo = re.findall(regex_string,circuit_memo)
        
        error = []
        error_memo = []
        for i,item in enumerate(res):
            if(item[0] != res_memo[i][0]) and (item[0] != res_memo[i][2]):
                error.append(item[0])
            if(item[2] != res_memo[i][0]) and (item[2] != res_memo[i][2]):
                error.append(item[2])
        for i,item in enumerate(res_memo):
            if(item[0] != res[i][0]) and (item[0] != res[i][2]):
                error_memo.append(item[0])
            if(item[2] != res[i][0]) and (item[2] != res[i][2]):
                error_memo.append(item[2])
                
        for i in range(len(error)):
            circuit = error[0]
            circuit_memo = error_memo[0]
            temp = circuit_dict_origin[circuit]
            temp2 = circuit_dict_origin[circuit_memo]        
            circuit_dict_origin[circuit_memo] = temp
            circuit_dict_origin[circuit] = temp2
    
    print(f"{circuit} <--> {circuit_memo}")
    return circuit_dict_origin

def check_circuit_matches(circuit_dict: dict, memo_cache: dict, circuit_dict_original: dict):
    
    for i,(key,val) in enumerate(sorted(circuit_dict.items(),key=lambda x : x)):  
        if(key[0] == "z" and key[1:].isdigit()):  
            # print(key[1:])
            is_equal, broken_wires = determine_errors(circuit_dict_original,memo_cache,(val,memo_cache[key]))
            # print()
            if not (is_equal):        
                print("We have a problem")
                print("=======================================================================================================================================================")                
                broken_wires = broken_wires[0]
                # print(broken_wires)                
                return broken_wires
    
    print("No error found in circuit")
    return None

def create_circuit_memo(circuit_dict : dict):
    memo_cache = {}    
    for i,(key,val) in enumerate(sorted(circuit_dict.items(),key=lambda x: x)):
        if(key[0] == "z" and key[1:].isdigit()):
            count = int(key[1:])
            if(count == 0):
                memo_cache[f"z{count:0>2}"] = f"[x{count:0>2} XOR y{count:0>2}]"
                memo_cache[f"c{count:0>2}"] = f"[x{count:0>2} AND y{count:0>2}]"
            elif(f"x{key[1:]}" not in circuit_dict):
                memo_cache[f"z{count:0>2}"] = f"{memo_cache[f"c{count-1:0>2}"]}"
            else:
                memo_cache[f"z{count:0>2}"] = f"[{memo_cache[f"c{count-1:0>2}"]} XOR [x{count:0>2} XOR y{count:0>2}]]"
                memo_cache[f"c{count:0>2}"] = f"[[x{count:0>2} AND y{count:0>2}] OR [{memo_cache[f"c{count-1:0>2}"]} AND [x{count:0>2} XOR y{count:0>2}]]]"    
    return memo_cache

def iterate_errors(circuit_dict):    
    circuit_dict_original =  copy.deepcopy(circuit_dict)
    circuit_dict = solve_circuit(circuit_dict)    
    memo_cache = create_circuit_memo(circuit_dict)
    res = check_circuit_matches(circuit_dict,memo_cache,circuit_dict_original)
    if(res != None):
        new_circuit_origin = fix_broken_wires(res[0],res[1],circuit_dict_original)
        iterate_errors(new_circuit_origin)
    else:
        return    

if __name__ == "__main__":
    fileName = "input1.csv"    
    circuit_dict = parsefile(fileName)    
    iterate_errors(circuit_dict)    