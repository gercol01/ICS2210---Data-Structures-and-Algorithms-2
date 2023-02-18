import queue
import random
from collections import defaultdict


#DFA
class DFA:
    #K = {S, A, B}
    #T = {a, b}
    #F = {B}
    #k1 = S
    # t = {(S, a) → A,(A, a) → B,(A, b) → S}

    final = [] #contains the final states of the DFA represented numerically

    #constructor
    def __init__(self, States, Alphabet, Initial_state, Final_states, Transitions):
        self.states = States
        self.alphabet = Alphabet
        self.initial_state = Initial_state
        self.final_states = Final_states #boolean
        self.transitions = Transitions
        self.Final() #creating the numeric representation of the final states

    def getTransitions(self):
        return self.transitions

    def getStates(self):
        return len(self.states)

    def Final(self):
        for x in range(0,len(self.final_states)):
            if self.final_states[x] == True:
                self.final.append(x)

    # computing the depth of the DFA, returns the cost to reach each Node
    def Search(self):

        visited = [] # array of nodes that have been visited
        
        queue = []  # queue which holds the nodes to be read
        
        # the first node to be seen is the initial one
        visited.append(self.initial_state) # mark the current node as visited
        queue.append(self.initial_state)
        costarray = [0] * n  # array, representing the cost to read each node

        while (len(queue) != 0):
            x = queue.pop(0)
            
            for next in self.transitions[x]:
                if next not in visited: #if it has not already been visited
                    visited.append(next)
                    queue.append(next)
                    costarray[next] = costarray[x] + 1 

        return costarray # returns the cost to reach each node

    # checking the depth, the traversal must end on a final state (including unreachable states, which will not effect the depth)
    def depth(self, Costarray):
        max = 0
        n = self.final

        for i in range(0, len(n)):
            if Costarray[n[i]] > max:
                max = Costarray[n[i]]

        return max  # returns the depth
    
    #The Hopcroft algorithm
    def hopcroft(self):
        # first step is to create 2 arrays, an array with Final and Non-Final Nodes
        final = []
        notfinal = []
        
        final = self.final #equal to the final states of the DFA
 
        for x in self.states:
            #if the value is not a final state it is marked as false
            if self.final_states[x] == False:
                notfinal.append(x)
 
        print("The states of the DFA are: " ,self.states)
        print("The final states of the DFA are: " ,final)
        print("The non-final states of the DFA are: " ,notfinal)
 
        #the group at the start of each iteration
        group1=[final,notfinal]
        group2=[]
 
        #the two groups will be of equal length
        while(len(group1))!=len((group2)):
    
            if(len(group2)!=0):
                group1=group2.copy()
                group2=[]
    
            #start checking transitions of states in each group, x is a group
            for x in group1:
    
                group3=[]
                group4=[]
    
                #y is a value in the group, checking if the transitions of y are in the same group as it is
                for y in x:
                    if(self.transitions[y][0] in x and self.transitions[y][1] in x):
                        group3.append(y)
                    else:
                        group4.append(y)
    
                if(len(group3)!=0):
                    group2.append(group3)
                if(len(group4) == 1):
                    group2.append(group4)
                elif(len(group4) > 1):

                    group5=[]
                    group6=[]

                    temp=group4[0]

                    #the transitions of the value temp
                    a=self.transitions[temp][0]
                    b=self.transitions[temp][1]

                    tempA=[]
                    tempB=[]

                    #checking the groups which the transitions belong to
                    #first checking the ones of temp
                    for x in group1:
                        if(a in x):
                            tempA = x
                        if(b in x):
                            tempB = x

                    #then checking the transitions of each value in group4
                    for y in group4:
                        if(self.transitions[y][0] in tempA and self.transitions[y][1] in tempB):
                            group5.append(y)
                        else:
                            group6.append(y)

                    #if the group of undistinguishable values is not empty
                    if(len(group5)!=0):
                        group2.append(group5)
                    if(len(group6)!=0):
                        group2.append(group6)

        #grouped
        #group1 is now a new list with partitions, values which are in the same group, have transitions which lead to the same pair of groups
        
        #the new states of the new dfa
        statesNew = []
        initialstateNew = ""
        Alpha = self.alphabet #symbols of the alphabet, i.e transition symbols
        TransitionsNew = {}

        finalstatesNew = []#numeric

        for x in group2:
            #Combine states
            #if the group only contains one value
            #Add states
            if(len(x) == 1):
                statesNew.append(x[0])

            else:
                if(x in statesNew):#only one
                    continue
                else:
                    statesNew.append(x[0])

            for y in x:
                #initial state
                if(y == self.initial_state):
                    if(len(x)==1):
                        initialstateNew = y
                    else:
                        initialstateNew = x[0]  #the first value of the group is taken as the initial group

                

                #final states
                for i in range(len(self.final)):
                    if(self.final[i] == y):
                        if(x in finalstatesNew):#if it already exists
                            break
                        else:
                            finalstatesNew.append(x)

                    else:
                        continue   

                temp = {} #is a dictionary used to store the transtions of the nodes

                #transitions
                if(len(x)==1):
                    TransitionsNew[y]=[self.transitions[y][0],self.transitions[y][1]]
                else:
                    TransitionsNew[x[0]]=[self.transitions[y][0],self.transitions[y][1]]
                    if(x[0] in temp):
                        continue

                    else:
                        temp[x[0]]=x

        
        #Creating the new transitions of the DFA
        for x in temp:
            for y in TransitionsNew:

                if(temp[x][0]==TransitionsNew[y][0]):
                    TransitionsNew[y][0]=x
                elif(temp[x][0]==TransitionsNew[y][1]):
                    TransitionsNew[y][1]=x
                elif(temp[x][1]==TransitionsNew[y][0]):
                    TransitionsNew[y][0]=x
                elif(temp[x][1]==TransitionsNew[y][1]):
                    TransitionsNew[y][1]=x

        finalStatesUtility = []
        finalNew = [False] * n #boolean states

        for x in finalstatesNew:
            F=x[0]
            finalStatesUtility.append(F)
        
        for x in finalStatesUtility:
            finalNew[x] = True #making the final node list
        
        return DFA(statesNew, Alphabet, initialstateNew, finalNew, TransitionsNew)

#the graph in question
class Graph:
    
    #constructor for graph
    def __init__(self,nodes):
        self.n = nodes #number of nodes
        self.transitions = defaultdict(list)# default dictionary to store transitions of the graph
        self.cost = 0 #the number of nodes visited to reach the current node
  
    # function to add edges
    def addTrans(self, A, N):
        self.transitions[A].append(N) #adding transition, one by one instead of a and b together

    #Depth First Search traversal
    def SCC(self):
        #initialise the nodes as not visited
        costarray = [-1] * (self.n) #stores the time to reach each node
        Minimum = [-1] * (self.n) #least amount of time to reach node
        CheckN = [False] * (self.n) #if the node is in the list or not
        NextS=[]
 
        #i are the different start points
        for i in range(self.n): #n are the nodes, hence 'i' is selecting the nodes
            if costarray[i] == -1:
                self.Node(i, Minimum, costarray, CheckN, NextS) #calling the iterative function to traverse the graph

    def Node(self,A, Minimum, costarray, CheckN, NextS):
        costarray[A] = self.cost #stores the time to reach each node
        Minimum[A] = self.cost
        self.cost += 1
        CheckN[A] = True #boolean list to see if a value is in the stack already
        
        NextS.append(A) #stores nodes while traversing
 
        # Go through the transitions of the node currently selected
        for N in self.transitions[A]:
            if costarray[N] == -1 : #-1 is the value if it has not been visited
             
                #finding the low link of each node, low link is the smallest id reachable from the node, including itself
                self.Node(N, Minimum, costarray, CheckN, NextS)
                Minimum[A] = min(Minimum[A], Minimum[N])

            #if the node is currently in the stack, stop traversal and calculate the minimum           
            elif CheckN[N] == True:
                Minimum[A] = min(Minimum[A], costarray[N])

        temp = []
        Cnode = -1 
        if Minimum[A] == costarray[A]:
            while Cnode != A: #until the starting node is reach, keep on adding
                #nodes here are sccs
                Cnode = NextS.pop()
                temp.append(Cnode)
                CheckN[Cnode] = False

            #node here are not sccs   
            listOfSccs.append(temp)

n = random.randint(16, 64)

# creating the states of the DFA, examples of state names are 0, 1, 2 ....N
States = []

for i in range(0, n):
    States.append(i)

#printing the states of the DFA
print("The states of the DFA are: ", States)

# creating the final/accepting states of the DFA

F = []
Final_states = []

for node in range(0,len(States)):
    x = bool(random.getrandbits(1))
    F.append(x)
    if x == True:
        Final_states.append(node)

print("The final states of the DFA are: ", Final_states)

# symbols of the alphabet
Alphabet = []

Alphabet.append('a')
Alphabet.append('b')

# creating the transitions
Transitions = {
    obj: [random.randint(0, n-1), random.randint(0, n-1)] for obj in States}

print("The transitions of the DFA is: ", Transitions)

# choosing the starting state

Initial_state = random.randint(0, n-1)

print("The initial state of the DFA is: ", Initial_state)

# Creating the DFA
DFA1 = DFA(States, Alphabet, Initial_state, F, Transitions)

Costarray1 = DFA1.Search() #returns the cost to reach each node

# checking which states are end states, traversal must end on an end state
print("The depth of the DFA is: ", DFA1.depth(Costarray1))
print("The number of states in the DFA: ", States)

DFA2 = DFA1.hopcroft()

Costarray2 = DFA2.Search() #returns the cost to reach each node

# checking which states are end states, traversal must end on an end state
print("The depth of the new DFA is: ", DFA2.depth(Costarray2))
print("The number of states in the new DFA: ", States)

listOfSccs = []

TG = DFA2.getTransitions()

print(TG)

graph = Graph(len(TG)*2) #each node has 2 transitions, each transition is divided

for key, value in TG.items():
    graph.addTrans(key,value[0]) #pointer a
    graph.addTrans(key,value[1]) #pointer b

graph.SCC()

#number of SCCS
print("The number of SCCs is: ", len(listOfSccs))

#number of states in the largest SCC
max = len(listOfSccs[0])

for i in listOfSccs:
    x = len(i)
    if x > max:
        max = x

print("The number of states in the largest SCC is: ", max)

min = len(listOfSccs[0])

for i in listOfSccs:
    y = len(i)
    if y < min:
        min = y

print("The number of states in the smallest SCC is: ", min)

