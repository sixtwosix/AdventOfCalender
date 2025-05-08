import tqdm
import re


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
            circuit[input[0]] = (int(input[1]),input[0])
    for gate in wire_gates:
        temp = gate[0].split()
        if(temp[0][0] == "y" and temp[0][1:].isdigit()) and (temp[2][0] == "x" and temp[2][1:].isdigit()):
            gate[0] = f"x{temp[0][1:]} {temp[1]} y{temp[0][1:]}"
        circuit[gate[1]] = (int(-1),gate[0])
    
    return circuit

def solve_circuit(circuit: dict):
    cache = {}
    
    def determine_val(node: str):
        n = list(circuit[node])
        if( n[0] != -1):
            return n
        else:            
            gate = tuple(n[1].split(" "))
            if(gate in cache):
                return cache[gate]
            val1 = determine_val(gate[0])
            val2 = determine_val(gate[2])
            if(gate[1] == "AND"):
                n[0] = val1[0] & val2[0]
                n[1] = f"[{val1[1]} AND {val2[1]}]"
            elif(gate[1] == "OR"):
                n[0] = val1[0] | val2[0]
                n[1] = f"[{val1[1]} OR {val2[1]}]"
            elif(gate[1] == "XOR"):
                n[0] = val1[0] ^ val2[0]
                n[1] = f"[{val1[1]} XOR {val2[1]}]"
        
            cache[gate] = n
            return n
    
    for key, val in tqdm.tqdm(circuit.copy().items()):
        if (val[0] == -1):
            circuit[key] = determine_val(key)
    
    return circuit

def determine_errors(circuit: dict, memo_circuit: dict, possible_errors):
    regex_string = r"\[(\w{3}) (XOR|AND|OR) (\w{3})\]"
    circuit = {v[1]: k for k, v in circuit.items()}
    memo_circuit = {v: k for k, v in memo_circuit.items()}
    cache = {}
    
    def reverse_engineer(statement: str, statement_memo: str):
        if((statement,statement_memo) in cache):
            return cache[(statement,statement_memo)]
        if(statement == statement_memo):
            n = True
            print(f"{statement} -- {statement_memo}")
        else:
            res = re.findall(regex_string,statement)
            res_memo = re.findall(regex_string,statement_memo)
            
            if(len(res) == 0 and len(res_memo) == 0):
                n = False
                print(f"{statement} -- {statement_memo}")
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
                        print(f"{statement} -- {statement_memo}")
                        return n
                        
                    y = circuit[x]
                    x = f"[{x1}]"
                    statement_memo = statement_memo.replace(x,y)
            
                # print(f"{statement} -- {statement_memo}")
            
                n = reverse_engineer(statement,statement_memo)
        cache[(statement,statement_memo)] = n
        return n
    
    return reverse_engineer(possible_errors[0],possible_errors[1])
    
    

if __name__ == "__main__":
    fileName = "input1.csv"
    
    circuit_dict = parsefile(fileName)
    circuit_dict_original = circuit_dict.copy()
    
    circuit_dict = solve_circuit(circuit_dict)
    
    # determine the memo
    memo_cache = {}    
    for i,(key,val) in enumerate(sorted(circuit_dict.items(),key=lambda x : x[0])):
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

    for i,(key,val) in enumerate(sorted(circuit_dict.items(),key=lambda x : x[0])):  
        if(key[0] == "z" and key[1:].isdigit()):  
            is_equal = determine_errors(circuit_dict_original,memo_cache,(val[1],memo_cache[key]))
            if not (is_equal):        
                print("We have a problem")
                print("=======================================================================================================================================================")
                break

    