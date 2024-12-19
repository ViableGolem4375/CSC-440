
import sys
import time

# Track time.
start_time = time.time()

# Check for bad file input.
try:
    file_name = sys.argv[1]
except IndexError:
    exit(1)

# Loops to populate lists of residents and hospitals to be used in the algorithm.
with open(file_name, "r") as f:
    n = int(f.readline())
    residents = {} 
    hospitals = {} 
    for i in range(n):
        line = f.readline().split() 
        resident = line[0] 
        preferences = line[1:] 
        residents[resident] = preferences
# Invariant: At any point in the loop, the number of items in the residents
# list will be less than or equal to 'range(n)'.
        
# Initialization: At the initialization of this for loop the list of 
# available residents will be empty (i.e. 0), and since 'range(n) cannot be
# negative, the invariant holds true.
        
# Maintenance: As elements are added to the residents list, the list grows
# in size as long as it is less than 'range(n)' meaning the invariant holds
# true.
        
# Termination: This loop terminates once i is no longer in range(n), and in this
# case the list will be filled with all available residents as range(n) is
# equal to the input size, this proving the invariant true.
        
    for i in range(n):
        line = f.readline().split() 
        hospital = line[0]
        preferences = line[1:]
        hospitals[hospital] = preferences
# Invariant: At any point in the loop, the number of items in the hospitals
# list will be less than or equal to 'range(n)'.
        
# Initialization: At the initialization of this for loop the list of 
# available hospitals will be empty (i.e. 0), and since 'range(n) cannot be
# negative, the invariant holds true.
        
# Maintenance: As elements are added to the hospitals list, the list grows
# in size as long as it is less than 'range(n)' meaning the invariant holds
# true.
        
# Termination: This loop terminates once i is no longer in range(n), and in this
# case the list will be filled with all available hospitals as range(n) is
# equal to the input size, this proving the invariant true.

matches = {}
free_residents = list(residents.keys())
proposals = {}

# Gale-Shapley Algorithm Code.
while free_residents: 
    resident = free_residents.pop(0) 
Instructor
| 02/07 at 2:04 pm
Grading comment:
This takes $n$ time and the while loop executes $n^2$ times. Hence this line takes a total of $n^3$.

    preferences = residents[resident] 
    if resident not in proposals: 
        proposals[resident] = 0 
    index = proposals[resident] 
    if index < n: 
        hospital = preferences[index] 
        proposals[resident] += 1 
        if hospital not in matches: 
            matches[hospital] = resident 
        else: 
            current = matches[hospital] 
            ranking = hospitals[hospital] 
            if ranking.index(resident) < ranking.index(current): 
                matches[hospital] = resident 
                free_residents.append(current)
            else:
                free_residents.append(resident)
# Invariant: At any point in the algorithm, for every hospital and every
# resident, if a hospital is removed from a resident's preference list, 
# then that hospital has a resident that it prefers over that resident.
                
# Initialization: This invariant is true before entering the loop as both 
# resident and hospital preference lists have not had any elements removed
# yet which fulfulls the invariant property.
                
# Maintenance: The list 'free_residents' consists of the list of available
# residents, through the loop a resident is removed from this list and 
# added to 'proposals' if it was not there already. This resident is then
# assigned to the 'index' variable which if it is less than 'n' (the input size),
# then it is added to the hospital's preference list. From here there are
# two cases, either the resident is crossed off of the preference list
# meaning that there is already another resident that hospital prefers to
# the current resident, or the resident is made the new preference if it is
# preferred to the old resident, in both cases the invariant holds true as
# the most preferred resident is always at the top spot.
                
# Termination: This loop terminates once the free_residents list has run 
# out of items, and if there are no more elements in this list that means
# the algorithm is complete and all residents have been paired with a
# hospital.

# Print out results.
for hospital, resident in matches.items():
    print(f"{resident} {hospital}")
time_complexity = time.time() - start_time
time_complexity_string = repr(time_complexity)
sys.stderr.write(time_complexity_string)
