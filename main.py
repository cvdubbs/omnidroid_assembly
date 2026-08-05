#import os
import sys
import config

sprokets_for_intermediate_assembly = {}
# Import the input.txt file and read its contents
with open(config.input_file, 'r') as file:
    # Read just the first line of two integers separated by a space
    input_data = file.readline().strip()
    # Split into two integer
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

# Set the recursion limit higher than n so the recursion does not stop early if the assembly chain of parts is very deep
sys.setrecursionlimit(n + 1000)

# Dict where key is 0 to n-1 and value is the list of parts that are used directly to build that part
req = {t: [] for t in range(n)}
# For each dependency, part i is used in the assembly of part j, so we add part i to the list for part j. The same part can be used more than once so we keep the duplicates
for i, j in dependencies:
    req[j].append(i)

# Dict where key is 0 to n-1 and value is the total number of sprockets needed to build that part including all the parts inside it. We store each part once we calculate it so we do not have to calculate it again every time the part is reused
cost = {}

def total_cost(t):
    # If we already calculated this part,  just return the stored value instead of calculating it again
    if t in cost:
        return cost[t]
    # Start with the number of sprockets used to attach this part's own pieces together
    running = sprokets_for_intermediate_assembly[t]
    # For each part required to build this part, add on that part's total number of sprockets
    for part in req[t]:
        running += total_cost(part)
    cost[t] = running
    return running

# This total is the number of sprockets for the whole assembly
answer = total_cost(n - 1)

# Write the total to output.txt
with open('output.txt', 'w') as out:
    out.write(str(answer))

print(answer)