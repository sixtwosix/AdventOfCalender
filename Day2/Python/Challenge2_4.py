if (__name__ == "__main__"):
    input_file = "./input1.csv"
    output_file = "./out3.csv"
    with open(input_file,'r') as f:  
        with open(output_file, 'w') as g:      
            lines = f.readlines()            
            count=0

            for elem in lines:

                levels = elem.split()
                prev = False
                safe = True
                increasing = False
                decreasing = False
                
                for item in levels:

                    item = int(item)

                    if prev != False:

                        if item > prev:
                            increasing = True

                            if item > (prev + 3):
                                safe = False

                        if item < prev:
                            decreasing = True

                            if item < (prev - 3):
                                safe = False

                        if item==prev:
                            safe= False

                    prev = item

                if (increasing == True and decreasing == True):
                    safe = False

                if safe == True:
                    count=count+1
                    g.write(elem)

                if safe == False:
                    
                    for i in range(len(levels)):

                        copy_of_levels = levels[:]
                        copy_of_levels.pop(i)

                        prev = False
                        safe=True
                        increasing = False
                        decreasing = False

                        for items in copy_of_levels:

                            items = int(items)

                            if prev != False: 
                                if items > prev:
                                    increasing = True

                                    if items > (prev + 3):
                                        safe = False

                                if items < prev:
                                    decreasing = True

                                    if items < (prev - 3):
                                        safe = False

                                if items==prev:
                                    safe= False

                            prev = items

                        if (increasing == True and decreasing == True):
                            safe = False

                        if safe == True:
                            count=count + 1
                            g.write(elem)
                            
                            break                      
        print(count)            