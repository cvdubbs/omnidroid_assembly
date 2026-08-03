import os
import config

sprokets_for_intermediate_assembly = {}
# Import the input.txt file and read its contents
with open(config.input_file, 'r') as file:
    # Read just the first line of two integers separated by a space
    input_data = file.readline().strip()
    # Split into two integers
    input_data = list(map(int, input_data.split()))
    # Integers n and m, indicating the number of parts in the assembly and the number of assembly dependencies
    n, m = input_data
    # For the next m lines, read the line and store it as a list of tuples
    dependencies = []
    for i in range(m):
        line = file.readline().strip()
        # Split the line into two integers and store as a tuple
        dependency_i_j = tuple(map(int, line.split()))
        dependencies.append(dependency_i_j)
    for j in range(n):
        # This line is one single integer, indicating the number of sprockets in the intermidate assembly
        num_sprockets = int(file.readline().strip())
        # Map of Assembly part number to the number of sprockets in the intermediate assembly
        sprokets_for_intermediate_assembly[j] = num_sprockets
# Sort the dependencies so the second element of the tuple puts everything in descending order and following that, the first element of the tuple puts everything in descending order
dependencies_sorted = sorted(dependencies,key=lambda x: (x[1], x[0]), reverse=True)
# Dict where key is 0 to n-1 and value is the total number of pieces needed for that part in the assembly
# Start with count of 0 for each key
dict_total_nodes = {i: 0 for i in range(n)}
dict_total_pieces = {i: 0 for i in range(n)}
# These tuples assmeble a tree that we need the count of leafs and the total number of each part in the assembly. Starts with the highest integer in the second position of the tuple.
# n-1 is always the head and will have a count of 1. The rest of the parts will have a count of 0. We will iterate through the sorted dependencies and for each dependency, 
# we will increment the count of the first element only if the next element matches

running_count = 1
prev_dependency = dependencies_sorted[0]
dict_total_nodes[prev_dependency[0]] = 1
dict_total_nodes[prev_dependency[1]] = 1
for dependency in dependencies_sorted[1:]:
    if dict_total_nodes[dependency[0]] == 0:
        dict_total_nodes[dependency[0]] = 1 * dict_total_nodes[dependency[1]]
    else:
        if dependency == prev_dependency:
            running_count += 1
            dict_total_nodes[dependency[0]] -= ((running_count -1) * dict_total_nodes[dependency[1]])
            dict_total_nodes[dependency[0]] += running_count * dict_total_nodes[dependency[1]]
        else:
            running_count = 1
            dict_total_nodes[dependency[0]] += 1 * dict_total_nodes[dependency[1]]

    prev_dependency = dependency

# Now that we have the total nodes counted, just multiply the total number of pieces for each part in the assembly by the number of sprockets in the intermediate assembly for that part
total_sprockets = 0
for assembly_part in dict_total_nodes.keys():
    dict_total_pieces[assembly_part] = dict_total_nodes[assembly_part] * sprokets_for_intermediate_assembly[assembly_part]
    total_sprockets += dict_total_pieces[assembly_part]
print("Total nodes for each part in the assembly:")
print(dict_total_nodes)
print("Total pieces for each part in the assembly:")
print(dict_total_pieces)
print("Total Sprockets for the entire assembly:")
print(total_sprockets)
