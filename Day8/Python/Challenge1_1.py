from itertools import permutations

G = {i+j*1j: c for i,r in enumerate(open('input1.csv'))
               for j,c in enumerate(r.strip())}

for i in range(50):
    str_line = ""
    for j in range(50):
        str_line+= G[i+j*1j]
    # print(str_line)



# for r in [1], range(50):
for r in [range(50)]:
# for r in [1]:
    anti = []
    for freq in {*G.values()} - {'.'}:
        print(freq)
        ants = [p for p in G if G[p] == freq]
        pairs = permutations(ants, 2)
        # print(list(pairs))
        # anti += [a+n*(a-b) for a,b in pairs
        #                    for n in r]
        # anti += [a+r*(a-b) for a,b in pairs]
        # anti = [a+r*(a-b) for a,b in pairs]
        anti = [a+n*(a-b) for a,b in pairs for n in r]
        antinodes = set(anti) & set(G)

        with open('output2_1.csv', 'a') as f:
            f.writelines(''.join([freq for z in range(50)]) + '\n')
            for i in range(50):
                str_line = ""
                for j in range(50):     
                    if((i+j*1j) in antinodes):
                        if(G[i+j*1j] == "."):
                            str_line+= "#"
                        else:
                            str_line+= G[i+j*1j]
                    else:
                        str_line+= G[i+j*1j]
                # print(str_line)
                f.writelines(str_line + "\n")


    all_antinodes = set(anti) & set(G)
    # print(all_antinodes)
    
    print(len(set(anti) & set(G)))

