
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
            

if __name__ == "__main__":
    fileName = "input1.csv"
    
    connections = parsefile(fileName)
    # print(connections)
    pc_map = map_connections(connections)
    trio_connect_list = map_trio_connections(pc_map)
    print(len(trio_connect_list))