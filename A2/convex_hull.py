
import math
import sys
from typing import List
from typing import Tuple
from functools import cmp_to_key

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]

mid = [0, 0]

def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def sort_clockwise(points: List[Point]):
    """
    Sorts `points` by ascending clockwise angle from +x about the centroid,
    breaking ties first by ascending x value and then by ascending y value.

    The order of equal points is not modified

    Note: This function modifies its argument
    """
    # Trivial cases don't need sorting, and this dodges divide-by-zero errors
    if len(points) < 2:
        return

    # Compute the centroid
    centroid_x = sum(p[0] for p in points) / len(points)
    centroid_y = sum(p[1] for p in points) / len(points)

    # Sort by ascending clockwise angle from +x, breaking ties with ^x then ^y
    def sort_key(point: Point):
        angle = math.atan2(point[1] - centroid_y, point[0] - centroid_x)
        normalized_angle = (angle + math.tau) % math.tau
        return (normalized_angle, point[0], point[1])

    # Sort the points
    points.sort(key=sort_key)

def quadrant(point):
    """
    Helper function to determine the quadrant of a point.
    """
    if point[0] >= 0 and point[1] >= 0:
        return 1
    if point[0] <= 0 and point[1] >= 0:
        return 2
    if point[0] <= 0 and point[1] <= 0:
        return 3
    return 4

def compare(p1, q1):
    """
    Helper function to compare points.
    """
    p = [p1[0] - mid[0], p1[1] - mid[1]]
    q = [q1[0] - mid[0], q1[1] - mid[1]]
    one = quadrant(p)
    two = quadrant(q)

    if one != two:
        if one < two:
            return -1
        return 1
    if p[1] * q[0] < q[1] * p[0]:
        return -1
    return 1

# Invariant: Assuming we have a list of tuples which correspond to points 
# in a 2D plane, at any point in the base_case_hull or compute_hull 
# algorithms, the output lists will not contain any points which are 
# not a part of the computed hull(s).

# Initialization: At the start time of the algorithm the output list of 
# points will be empty meaning it does not contain any points that are not
# on the hull, thus the invariant holds true.

# Maintenance: Assuming the invariant is true for each divide step, this 
# step is done recursively until it hits the base case. If the base case is 
# reached then this means a hull has been reached with 3 or less points in 
# which case the invariant is true as in a convex hull of 3 or less points, 
# all points will be on the hull. If the base case is not reached, the 
# algorithm will run recursively through the lists. During this process
# the algorithm will be computing upper and lower tangent values for each
# sub-hull computed, this is done as follows:
#     - Left hull: pick highest x value.
#     - Right hull: pick lowest x value.
#     - Find the y intercept, move left counter clockwise and right 
#       clockwise, do this repreately until you find highest y-intercept.
#     - Do the same for lower tanget but instead reverse the work
#     - If the base case is true, then we assume this is also true, 
#       which leads us to getting the smallest set of convex hull.
# During this process the invariant will hold true for all hulls as any
# points which are not a part of the hull are thrown out in favor of ones
# that are via the tangent computing until the base case is reached in
# which case the invariant holds true as per the explanation above.

# Termination: This algorithm terminates when it is done making comparisons 
# to find the upper tangest, lower tangents, etc. Then returns the smallest 
# set of points in clockwise order that make up the convex hull, and as per
# the explanation of the base case in the Maintenance section, the 
# invariant holds true in this case.

def base_case_hull(points: List[Point]) -> List[Point]:
    """ 
    Base case of the recursive algorithm.
    """
    if len(points) == 0:
        return points
    if len(points) <= 3:
        sort_clockwise(points)
        return points

    hull = []
    for index1, point1 in enumerate(points):
        on_hull = False

        for index2, point2 in enumerate(points):
            if index1 == index2: continue
            correct = 0
            if point1[0] == point2[0]:
                correct = point_checker_for_equal_points(points, point2)
            else:
                correct = point_checker(points, point1, point2)

            if correct: 
                on_hull = True
                break

        if on_hull:
            hull.append(point1)

    sort_clockwise(hull)
    return hull

def point_checker(points, point1, point2):
    correct1 = True
    correct2 = True

    for point in points :
        if point == point1 or point == point2:
            continue
        y_int = y_intercept(point1, point2, point[0])

        if y_int < point[1]:
            correct1 = False
        elif y_int > point[1]:
            correct2 = False
    
    if correct1 or correct2:
        return True
    else:
        return False

def point_checker_for_equal_points(points, point2):
    correct1 = True
    correct2 = True
    for point in points :
        if point2[0] < point[0]:
            correct1 = False
        elif point2[0] > point[0]:
            correct2 = False

    if correct1 or correct2:
        return True
    else:
        return False

def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    if len(points) < 7:
        return base_case_hull(points)
    
    points.sort()
    hull = divide(points)

    return hull

def divide(points: List[Point]):
    if len(points) < 6:
        return base_case_hull(points)

    midpoint = len(points) // 2

    while(points[midpoint + 1][0] == points[midpoint][0]):
        midpoint += 1
        if midpoint == (len(points) - 1):
            return base_case_hull(points)
            left = divide(points[0:midpoint + 1])
    right = divide(points[midpoint + 1:])

    hull = merge_hulls(left, right)

    return hull

def is_colinear(points):
    ho = True
    vert = True
    for i in range(len(points)-1):
        if points[i][0] != points[i+1][0]:
            vert = False
        if points[i][1] != points[i+1][1]:
            ho = False
        if (not vert) and (not ho):
            return False

    return True

def merge_hulls(left: List[Point], right: List[Point]) -> List[Point]:
    """
    Function to find the upper and lower tangents, then merge.
    """

    #sort_clockwise(left)
    #sort_clockwise(right)

    if is_colinear(left) or is_colinear(right):
        return base_case_hull(left + right)
        i = left.index(max(left))
    j = right.index(min(right))
    k = i
    l = j
    
    middle = (left[i][0] + right[j][0]) / 2

    # Finds the upper tangent.
    upper = [left[i], right[j]]
    while(True):
        y_int = y_intercept(upper[0], upper[1], middle)

        if y_intercept(left[(i - 1) % len(left)], upper[1], middle) < y_int:
            i -= 1
            upper[0] = left[i%len(left)]
        elif y_intercept(upper[0], right[(j + 1) % len(right)], middle) < y_int:
            j += 1
            upper[1] = right[j % len(right)]
        else:
            break

    # Finds the lower tangent.
    lower = [left[k], right[l]]
    while(True):
        y_int = y_intercept(lower[0], lower[1], middle)

        if y_intercept(left[(k + 1) % len(left)], lower[1], middle) > y_int:
            k += 1
            lower[0] = left[k % len(left)]
        elif y_intercept(lower[0], right[(l - 1) % len(right)], middle) > y_int:
            l -= 1
            lower[1] = right[l % len(right)]
        else:
            break
    
    hull = []
    
    counter1 = k
    while(True):
        hull.append(left[counter1 % len(left)])
        if left[counter1 % len(left)] == upper[0]:
            break
        counter1 += 1

    counter2 = j
    while(True):
        hull.append(right[counter2 % len(right)])
        if right[counter2 % len(right)] == lower[1]:
            break
        counter2 += 1
     
    return hull
