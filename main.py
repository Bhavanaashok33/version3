from getAdjacencyList import getAdjacencyList
from get_R_Q_matrices import get_initial_R_matrix
from get_R_Q_matrices import get_initial_Q_matrix
from getResult import getResult

import pandas as pd

def main():    
    data = pd.read_csv("graph.csv")
    graph = getAdjacencyList(data)
    
    A = graph["A"]
    Z = graph["Z"]
    weight = graph["weight"]
    A_Z_dict = graph["A_Z_dict"]
    
    src = 1
    dest = [9]
    R = get_initial_R_matrix(A, Z, weight, A_Z_dict)
    Q = get_initial_Q_matrix(R)
    
    alpha = 0.7 # learning rate
    epsilon = 0.1 # greedy policy
    n_episodes = 1000 # no of episodes
    
    result = getResult(R, Q, alpha, epsilon, n_episodes, src, dest)
    return result
    # print("Destination =", result["ends_find"])
    # for key, value in result["cost"].items():
    #     print("Total cost =", key)
    #     print("No of paths with cost {} = {}".format(key,value))
    # #print(result["routes_number"])
    # print("Paths =",result["all_routes"])


# if '__name__'=='__main__':
#     main()
