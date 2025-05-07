import tqdm



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


if __name__ == "__main__":
    fileName = "input1.csv"
    
    circuit_dict = parsefile(fileName)
    
    circuit_dict = solve_circuit(circuit_dict)
    
    # for key in circuit_dict.keys():
    #     print(f"'{key}' : {circuit_dict[key]}")
    
    memo_cache = {}
    
    for i,(key,val) in enumerate(sorted(circuit_dict.items(),key=lambda x : x[0])):
        if(key[0] == "z" and key[1:].isdigit()):
            count = int(key[1:])
            if(count == 0):
                memo_cache[f"z{count:0>2}"] = f"[x{count:0>2} XOR y{count:0>2}]"
                memo_cache[f"c{count:0>2}"] = f"[x{count:0>2} AND y{count:0>2}]"
            else:
                memo_cache[f"z{count:0>2}"] = f"[{memo_cache[f"c{count-1:0>2}"]} XOR [x{count:0>2} XOR y{count:0>2}]]"
                memo_cache[f"c{count:0>2}"] = f"[[x{count:0>2} AND y{count:0>2}] OR [[x{count:0>2} XOR y{count:0>2}] AND {memo_cache[f"c{count-1:0>2}"]}]]"
            if(val[1] != memo_cache[key]):
                print(f"{key} : {val[1]} -- {memo_cache[key]}")