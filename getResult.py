from QRouting import QRouting

from routeHelpers import getBestNodeInPath
from routeHelpers import getBestSubgraph
from routeHelpers import getAllBestPaths
from routeHelpers import getCost
from routeHelpers import countPaths
from routeHelpers import getPath

from collections import Counter

def getResult(R, Q, alpha, epsilon, n_episodes, start, end):
    Q = QRouting(R, Q, alpha, epsilon, n_episodes, start, end)
    # print "The Q values are: {}".format(Q)
    nodes = getBestNodeInPath(Q, start, end)
    graph = getBestSubgraph(Q, nodes)
    route_len = len(getPath(Q, start, end))
    paths = getAllBestPaths(graph, start, end, route_len + 1)
    result = countPaths(paths)

    ends_find = []
    for i in range(len(paths)):
        ends_find.append(paths[i][-1])
    ends_find = list(set(ends_find))

    cost = []
    for i in paths:
        cost.append(getCost(R, i))
    Counter(cost)

    return {"nodes":nodes,
            "graph":graph,
            "ends_find":ends_find,
            "cost":dict(Counter(cost)),
            "routes_number":result['routes_number'],
            "all_routes":result['all_routes']}