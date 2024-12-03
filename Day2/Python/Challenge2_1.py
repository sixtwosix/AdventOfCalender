import pandas as pd
import numpy as np

data = pd.read_csv('test_input1.csv')
data['Reports'] = data['Reports'].apply(lambda x: x.split())

def is_strictly_increasing(report):
    return [0 if (int(x) < int(y)) else 1 for x,y in zip(report,report[1:])]

def is_strictly_decreasing(report):
    return [0 if (int(x) > int(y)) else 1 for x,y in zip(report,report[1:])]

def step_change(report):
    return [0 if (abs(int(x) - int(y)) < 4) else 1 for x,y in zip(report,report[1:])]    
    

data['Increasing'] = data['Reports'].apply(is_strictly_increasing) * 1
data['Increasing_sum'] = data['Increasing'].apply(sum)
data['Decreasing'] = data['Reports'].apply(is_strictly_decreasing) * 1
data['Decreasing_sum'] = data['Decreasing'].apply(sum)
data['StepChange'] = data['Reports'].apply(step_change) * 1
data['StepChange_sum'] = data['StepChange'].apply(sum)

# Check for faults and remove data point






# data['ConditionMet'] = ((data['Increasing'] + data['Decreasing']) * data['StepChange'])

print(data)