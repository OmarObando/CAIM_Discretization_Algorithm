from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
#fetch dataset
iris = fetch_ucirepo(id=53)

X = iris.data.features
y = iris.data.targets

iris_data = pd.concat([X, y], axis=1)
iris_data = iris_data[['petal length', 'class']]

# Obtener la longitud del pétalo
petals_length = X[X.columns[2]].tolist()
# Get Max and Min values
min_petal_length = min(petals_length)
max_petal_length = max(petals_length)
#Get unique values and sort them
unique_petals_length = set(petals_length)
unique_petals_length = sorted(unique_petals_length)
#Get inner intervals
##Generate intervals function
def generate_interval_boundaries(values, min_value, max_value):
    boundaries = []
    boundaries.extend([min_value, max_value])
    num_values = len(values)
    for i in range(num_values - 1):
        interval_average = (values[i] + values[i + 1]) / 2
        boundaries.append(interval_average)
    boundaries.sort()
    return boundaries

##Generate inner intervals
inner_intervals = generate_interval_boundaries(unique_petals_length, min_petal_length, max_petal_length)
##Set global variables
D = [min_petal_length, max_petal_length]
cut_points = []
B = inner_intervals
GLOBAL_CAIM = 0
F = iris_data
CLASES = y[y.columns[0]].unique()
##Calculate CAIM function


def calculate_CAIM_measure(scheme, cut_points, values):
    ##Calculate matrix of quanta
    cut_points = sorted(cut_points)
    data_of_intervals = []
    ##Get the first interval
    data_of_intervals.append(values[values.iloc[:, 0] <= cut_points[0]])
    ##Get the inner intervals
    for i in range(len(cut_points) - 1):
        data_of_intervals.append(values[(values.iloc[:, 0] > cut_points[i]) & (values.iloc[:, 0] <= cut_points[i + 1])])
    ##Get the last interval
    data_of_intervals.append(values[values.iloc[:, 0] > cut_points[-1]])
    ##Get Classes
    quanta_matrix = []
    for inteval in data_of_intervals:
        row = []
        for clase in CLASES:
            row.append(len(inteval[inteval.iloc[:, 1] == clase]))
        quanta_matrix.append(row)
    quanta_matrix = np.array(quanta_matrix)
    ##Calculate the CAIM measure
    ##Calculate the sum
    matrix_sum = 0
    # print(len(quanta_matrix))
    for i in range(len(quanta_matrix)):
        # print(quanta_matrix)
        sum_row = sum(quanta_matrix[i].tolist())
        max_value_row = max(quanta_matrix[i].tolist())
        # print(max_value_row)
        # # print(sum_row)
        
        matrix_sum += pow(max_value_row, 2)/sum_row if sum_row != 0 else 0
    caim_value = matrix_sum/len(quanta_matrix)
    return caim_value

##Define intervals acoording to the numbers of classes
def main_1():
    global GLOBAL_CAIM
    global cut_points
    global B
    global D
    global F
    global CLASES
    global iris_data
    for i in range(len(B)):
        caim_values = []
        for j in range(len(B)):
            if B[j] not in cut_points:
                cut_points.append(B[j])
                caim_values.append(calculate_CAIM_measure(D, cut_points, F))
                cut_points.pop()
        max_value = max(caim_values)
        if max_value > GLOBAL_CAIM:
            GLOBAL_CAIM = max_value
            cut_points.append(B[caim_values.index(max_value)])
        else:
            break
    print("The best cut points are: ", cut_points)
    print("The best CAIM value is: ", GLOBAL_CAIM)
    return cut_points, GLOBAL_CAIM
   
##Define intervals acoording of the CAIM measure
def main_2():
    global GLOBAL_CAIM
    global cut_points
    global B
    global D
    global F
    global CLASES
    global iris_data
    caim_values = []
    flag = True
    while flag == True:
        flag = False
        for i in range(len(B)):
            if B[i] not in cut_points:
                cut_points.append(B[i])
                caim_values.append(calculate_CAIM_measure(D, cut_points, F))
                cut_points.pop()
        max_value = max(caim_values)
        if max_value >= GLOBAL_CAIM:
            flag = True
            GLOBAL_CAIM = max_value
            cut_points.append(B[caim_values.index(max_value)])
            caim_values = []

    print("The best cut points are: ", cut_points)
    print("The best CAIM value is: ", GLOBAL_CAIM)
    return cut_points, GLOBAL_CAIM


main_2()

##Var to discretize petal length (F)
##

