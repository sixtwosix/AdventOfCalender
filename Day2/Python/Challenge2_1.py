import pandas as pd
import numpy as np

data = pd.read_csv('test_input1.csv')
data['Reports'] = data['Reports'].apply(lambda x: x.split())

def is_strictly_increasing(report):
    return all(int(x) < int(y) for x,y in zip(report,report[1:]))

def is_strictly_decreasing(report):
    return all(int(x) > int(y) for x,y in zip(report,report[1:]))

def step_change(report):
    return all(abs(int(x) - int(y)) < 4 for x,y in zip(report,report[1:]))

data['Increasing'] = data['Reports'].apply(is_strictly_increasing) * 1
data['Decreasing'] = data['Reports'].apply(is_strictly_decreasing) * 1
data['StepChange'] = data['Reports'].apply(step_change) * 1

data['ConditionMet'] = ((data['Increasing'] + data['Decreasing']) * data['StepChange'])

print(data)