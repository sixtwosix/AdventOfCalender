import polars as pl

df = pl.read_csv("./input1.csv",has_header=False)

print(df)

series_input1 = df.to_series(0)
series_input2 = df.to_series(1)

# list_input1 = [3,4,2,1,3,3]
# list_input2 = [4,3,5,3,9,3]
list_input1 = series_input1.to_list()
list_input2 = series_input2.to_list()

list_input1.sort()
print(list_input1)
list_input2.sort()
print(list_input2)

list_difference = []

for i in range(len(list_input1)):
    x = abs(list_input2[i] - list_input1[i])
    list_difference.append(x)
    
print(list_difference)

print(sum(list_difference))