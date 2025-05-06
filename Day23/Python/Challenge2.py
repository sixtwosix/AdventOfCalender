import tqdm

def parsefile(fileName: str) -> list:
    with open(fileName, 'r') as f:
        connections = f.readlines()
        
        connections = list(map(lambda x: x.strip().split("-"),connections))
    
    return connections


def map_connections(connections: list[list[str]]) -> dict:
    
    connect_map = {}
    for connect in connections:
        pc1,pc2 = connect
        if(pc1 not in connect_map):
            connect_map[pc1] = []
        if(pc2 not in connect_map):
            connect_map[pc2] = []
        
        connect_map[pc1] += [pc2]
        connect_map[pc2] += [pc1]
    
    return connect_map

def map_trio_connections(connect_map: dict) -> list:
    
    trio_connect_list = []
    
    for key1, val1 in connect_map.items():
        for key2, val2 in connect_map.items():
            for key3, val3 in connect_map.items():
                if(key1 != key2) and (key2 != key3) and (key3 != key1):
                    if ( ((key1 in val2) and (key1 in val3)) and
                        ((key2 in val1) and (key2 in val3)) and
                        ((key3 in val1) and (key3 in val2))
                    ):
                        temp = [key1,key2,key3]
                        temp = sorted(temp)
                        if(temp not in trio_connect_list):
                            if('t' == key1[0]) or ('t' == key2[0]) or ('t' == key3[0]):
                                trio_connect_list.append(temp)
                                # print(f"{key1} -- {key2} -- {key3}")
    
    return trio_connect_list

def determine_all_lan_parties(connect_map: dict) -> list:
    lan_party = []
    cache = {}
    
    def determine_party(possible_party: list):
        n = []
        if(tuple(possible_party) in cache):
            return cache[tuple(possible_party)]
        if(len(possible_party) == 1):
            # final condition met, return
            n += [possible_party]
        else:
            for pc in possible_party:
                connections = connect_map[pc]
                connect_match = list(set(connections) & set(possible_party))
                for item in determine_party(connect_match):
                    item = sorted(item + [pc])
                    if(item not in n):
                        n += [item]
        cache[tuple(possible_party)] = n
        return n
    
    for key, val in tqdm.tqdm(connect_map.items()):
        res = determine_party(val)
        res = [ sorted(item + [key]) for item in res]
        for item in res:
            if(item not in lan_party):                
                lan_party.append(item)
    
    return lan_party
                
            

if __name__ == "__main__":
    fileName = "input1.csv"
    
    connections = parsefile(fileName)
    
    print("mapping connections...")
    pc_map = map_connections(connections)
    print("determining lan parties...")
    lan_parties = determine_all_lan_parties(pc_map)
    print("determining biggest party...")
    max_party_size = 0
    party_pcs = []
    for party in lan_parties:
        if(len(party) > max_party_size):
            max_party_size = len(party)
            party_pcs = party
    
    print(f"Max party size {max_party_size} with passcode:\n{",".join(party_pcs)}")