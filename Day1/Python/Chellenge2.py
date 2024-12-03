import polars as pl

df = pl.read_csv("./input1.csv",has_header=False)

series_input1 = df.to_series(0)
series_input2 = df.to_series(1)

list_input1 = series_input1.to_list()
list_input2 = series_input2.to_list()

list_output = []

for x in list_input1:
    occurences = list_input2.count(x)
    list_output.append(occurences * x)
    
print(sum(list_output))