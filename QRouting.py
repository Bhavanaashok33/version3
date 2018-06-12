from routeHelpers import getBestNodeInPath

import random

# Update Q matrix
def update_Q(T,Q,current_state, next_state, alpha):
    current_t = T[current_state][next_state]
    current_q = Q[current_state][next_state]
    new_q = current_q + alpha * (current_t + min(Q[next_state].values()) - current_q)
    Q[current_state][next_state] = new_q   
    return Q

# This helper function returns the <key>, from dictionary, for which the <value> is minimum.
def getKeyOfMinValue(dic):
        min_val = min(dic.values())
        return [k for k, v in dic.items() if v == min_val]

# Main algorithm
def QRouting(T, Q, alpha, epsilon, n_episodes, start, end):
    nodes_number = [0,0]
    for e in range(n_episodes):
        if e in range(0,n_episodes,1000):
            #print("loop:",e)
            pass
        current_state = start
        goal = False
        while not goal:
            valid_moves = list(Q[current_state].keys())
            
            if len(valid_moves) <= 1:
                next_state = valid_moves[0]
            else:
                best_action = random.choice(getKeyOfMinValue(Q[current_state]))
                if random.random() < epsilon:
                    valid_moves.pop(valid_moves.index(best_action))
                    next_state = random.choice(valid_moves)
                else:
                    next_state = best_action
            Q = update_Q(T,Q,current_state, next_state, alpha)
            if next_state in end:
                goal = True
            current_state = next_state

        if e in range(0,1000,200):
            for i in Q.keys():
                for j in Q[i].keys():
                    Q[i][j] = round(Q[i][j],6)
            nodes = getBestNodeInPath(Q, start, end)

            nodes_number.append(len(nodes))
            if len(set(nodes_number[-3:])) == 1:
                break
    return Q
    
