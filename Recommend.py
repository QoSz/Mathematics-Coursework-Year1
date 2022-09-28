import numpy as np
import time

# from numba import jit

start = time.time()
# Getting all the values in the file accept the first line and creating a list
history_file = open("history.txt", "r")
# Getting values of the first line
first_line = history_file.readlines(1)
X = list(map(int, first_line[0].split()))
lines = [list(map(int, line.split())) for line in history_file][0:]
*T, = map(list, {*map(tuple, lines)})
print(f"Positive entries: {len(T)}")
No_items = X[1]
No_Customers = X[0]
history_file.close()

# Creating a zeros array then adding the values of 1 in the correct position
vectors = np.zeros((No_items, No_Customers))
rows = [i[1] - 1 for i in lines]
# print(rows)
columns = [x[0] - 1 for x in lines]
# print(columns)
vectors[rows, columns] = 1
# Calculating the number of vector created in the vectors array
number_of_vectors = len(vectors) * (len(vectors) - 1)


# @jit(nopython=True)
def calculate_angle(x, y):
    theta = np.degrees(np.arccos(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))))
    return theta


# # Calculating the Average angle
total = sum(calculate_angle(vectors[i], vectors[j]) for i in range(No_items) for j in range(No_Customers) if i != j)
print(f"Average angle: {round(total / number_of_vectors, 2)}")


# Calculating the min angle for the queries file
def angles(a, b):
    min_angles = []
    if a != '':
        for i in range(1, int(No_items) + 1):
            if str(i) not in b:
                min_angles.append([i, (calculate_angle(vectors[(int(a) - 1)], vectors[(i - 1)]))])

    def function(x):
        return x[1]

    return sorted(min_angles, key=function)[0]


# # Sorting the items
def recommended_item(z):
    def function(x):
        return x[0]

    order = sorted(z, key=function)
    output = ""
    for i in order:
        output += ' ' + str(i[1]) + ' '
    return output


queries_file = open("queries.txt", "r")
read_query = queries_file.readlines()
query_list = [i.strip() for i in read_query]
# Looping through the queries file and printing the shopping cart items
for i in query_list:
    print(f"Shopping cart: {i}")
    recommend = []
    found_updated = []
    query_items = list(i.split(' '))
    for x in query_items:
        match, angle = angles(x, i)
        if angle > 90:
            continue
        elif match not in found_updated:
            recommend.append([angle, match])
            found_updated.append(match)
        if angle < 90:
            print(f"Item: {x}; match: {match}; angle: {round(angle, 2)}")
        else:
            print(f"Item: {x} no match")
    print(f"Recommend: {recommended_item(recommend)}")
queries_file.close()
end = time.time()
print(f"The time taken to run the code was: {start - end}")
