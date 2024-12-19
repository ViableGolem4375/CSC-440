# I have completed the extra credit portion of this assignment and uploaded
# it in a .pdf file titled extra_credit.pdf

# Imports.
from typing import List
from typing import Optional
from rubik import perm_apply, perm_inverse

import rubik
import heapq
from collections import deque

'''
Invariant Documentation:

Definition: The "frontier" for this algorithm will always be reachable 
            within i-1 hops, likewise, the "next level" will always be 
            reachable within i hops.

Initialization: At initialization, both the frontier and the next level
                are both empty because no vertices have been explored
                and nothing has been added to either list, thus the 
                invariant holds true as both are reachable within i-1
                hops (because they're both currently reachable in 0 hops
                due to being empty).

Maintenance: At each iteration of the algorithm, the frontier is expanded
             by looking at all edges stemming from vertices at the current
             frontier. When we move from one level to the next, vertices
             that are reachable in i hops from the source vertex are added
             to the frontier. Since only unvisited vertices are considered,
             the frontier maintains this property and the invariant holds
             true.

             For the next level, this contains the vertices which will be 
             explored in the next iteration. When vertices from the current
             frontier are processed, we add their neighbors to the next 
             level. These neighbors are accessible in i hops from the 
             source vertex (i.e. one more than the frontier which is i-1),
             and by construction, the next level is reachable in i hops,
             thus the invariant holds true.
    
Termination: If it finds a path from start to end, then it returns the 
             path it found, thus the invariant holds true. Otherwise it 
             will keep checking for paths until all options have been 
             exhausted, if this happens then there is no available pathway 
             and all options have been exhausted, thus the invariant holds 
             true either way. 
'''      

# Class to store the state of the node.
class node_info:
    def __init__(self, state, parent, order):
        self.state = state
        self.parent = parent
        self.order = order

# Gets the next frontier.
def find_next_frontier(frontier, nodes):
    start = frontier[0].order

    while start == frontier[0].order:
        current = frontier.popleft()

        # Changes the rubik state.
        for move in rubik.quarter_twists:
            move_state = rubik.perm_apply(move, current.state)
            # Checks to see if the new move_state is not in the nodes list.
            if move_state not in nodes:
                # New node_info with the new move_state, the move command it took
                # frontier that was popped, and the new depth of node.
                new_state = node_info(move_state, (move, current), current.order + 1)
                frontier.append(new_state)
                nodes.append(move_state)

# Main algorithm.
def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """

    # Start side of BFS.
    start_initialization = node_info(start, (None, None), 0)
    start_frontier = deque([start_initialization])
    start_parents = []

    # End side of BFS.
    end_initialization = node_info(end, (None, None), 0)
    end_frontier = deque([end_initialization])
    end_parents = []

    # Flag variable to determine which side the frontier changes on.
    flag = 1

    # This checks to see if both sides are the same to return an empty list.
    for left_current in start_frontier:

        for right_current in end_frontier:
            if left_current.state == right_current.state:
                return []

    found = False

    while not found:

        if start_frontier[0].order > 6 and end_frontier[0].order > 6:
            return None

        if flag == 1:
            # Gets the next frontier.
            find_next_frontier(start_frontier, start_parents)
            flag = flag * (-1)
        else:
            # Gets the next frontier.
            find_next_frontier(end_frontier, end_parents)
            flag = flag * (-1)

        # Grabs a left element from the starting frontier.
        for left_current in start_frontier:
         
            # Compares it to each of the right elements from the end frontier.
            for right_current in end_frontier:
                # If we find an element that matches.
                if left_current.state == right_current.state:
                    # Find the intersect of the two lists.
                    intersection = (left_current, right_current)
                    # We set found to true.
                    found = True
                    # Then break out of the loop.
                    break
            # If the element was found we can break out of this loop as well.
            if found == True:
                break
    # Solution list.
    solution = []

    left_temp = intersection[0]
    
    # These while loops populate the solution list.
    while (left_temp.state != start):
        solution.insert(0, left_temp.parent[0])
        left_temp = left_temp.parent[1]

    right_temp = intersection[1]

    while (right_temp.state != end):
        solution.append(rubik.perm_inverse(right_temp.parent[0]))
        right_temp = right_temp.parent[1]

    return solution
