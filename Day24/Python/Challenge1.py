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
        circuit[input[0]] = int(input[1])
    for gate in wire_gates:
        circuit[gate[1]] = gate[0]
    
    return circuit

def solve_circuit(circuit: dict):
    cache = {}
    
    def determine_val(node: str):
        n = circuit[node]
        if(isinstance(n,int)):
            return n
        else:            
            gate = tuple(n.split(" "))
            if(gate in cache):
                return cache[gate]
            val1 = determine_val(gate[0])
            val2 = determine_val(gate[2])
            if(gate[1] == "AND"):
                n = val1 & val2
            elif(gate[1] == "OR"):
                n = val1 | val2
            elif(gate[1] == "XOR"):
                n = val1 ^ val2
        
            cache[gate] = n
            return n
    
    for key, val in tqdm.tqdm(circuit.copy().items()):
        if isinstance(val,str):
            circuit[key] = determine_val(key)
    
    return circuit


if __name__ == "__main__":
    fileName = "input1.csv"
    
    circuit_dict = parsefile(fileName)
    
    circuit_dict = solve_circuit(circuit_dict)
    
    print(circuit_dict)
    
    binary_number = []
    final_val = 0
    
    # print(sorted(circuit_dict.items(),key=lambda x: x[0]))
    
    for i,(key,val) in enumerate(circuit_dict.items()):
        if(key[0] == "z" and key[1:].isdigit()):
            final_val = final_val ^ ( val << int(key[1:]))
            binary_number.insert(0,val)
            
    print(binary_number)
    print(final_val)