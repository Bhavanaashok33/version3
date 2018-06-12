from collections import Counter

#  Helper function to return the list of <key> for each of the Q[state] whose <value> is minimum
def getDictWithMinValues(dic):
    single_link = {}
    min_value = min(dic.values())
    for key in dic.keys():
        if dic[key] == min_value:
            single_link[key] = dic[key]
    return single_link.keys()

#  Helper function used to eliminate non-relevant nodes while traversing from src to dst.
def getBestNodeInPath(Q, start, end):
    next_level = [start]
    node_use = [start]
    while list(set(next_level) & set(end)) == []:
        temp_level = []
        for i in next_level:
            temp_level += getDictWithMinValues(Q[i])     # e.g. returns [3,4] initially
        next_level = list(set(temp_level))
        node_use += next_level
    return list(set(node_use))

# Helper function to generate a subgraph containing all the nodes that we found in the best path from the
# src to dest.
def getBestSubgraph(Q, nodes):
    best_net = {}
    for i in nodes:
        x = getDictWithMinValues(Q[i])
        best_net[i] = list(set(x) & set(nodes))
    return best_net

# Helper function used to generate the best paths from src to dest. Multiple paths can also be generated
def getAllBestPaths(graph, start, end, max_depth):
    past_path = []
    queue = []
    queue.append([start])
    while queue:
        path = queue.pop(0)
        node = path[-1]
        for adjacent in graph.get(node, []):
            newPath = list(path)
            if adjacent in end:
                newPath.append(adjacent)
                past_path.append(newPath)
                continue
            
            if adjacent in newPath:
                continue

            newPath.append(adjacent)
            if len(newPath) >= max_depth and newPath[-1] not in end:
                break
            queue.append(newPath)
            past_path.append(newPath)

    best_paths = []
    for l in past_path:
        if l[-1] in end:
            best_paths.append(l)

    return best_paths
    
# Helper function to get cost of the path
def getCost(R, route):
    cost = 0
    for i in range(len(route)-1):
        cost += R[route[i]][route[i+1]]
    return round(cost,3)

# Helper function used to count the number of best paths passed to it as an argument
def countPaths(paths):
    ends_find = []
    all_routes = {}
    for i in range(len(paths)):
        ends_find.append(paths[i][-1])

    count =  dict(Counter(ends_find))
    
    ends = list(set(ends_find))
    for i in ends:
        all_routes[i] = []
    for i in paths:
        end = i[-1]
        all_routes[end].append(i)

    return {"routes_number":count,
            "all_routes":all_routes}
    
        
# Helper function used to construct the path from src to dest using Q matrix.
def getPath(Q, start, end):
    single_route = [start]
    while single_route[-1] not in end:
        next_step = min(Q[single_route[-1]],key=Q[single_route[-1]].get)
        single_route.append(next_step)
        if len(single_route) > 2 and single_route[-1] in single_route[:-1]:  # to handle loops, if loop break
            break
    return single_route




















    