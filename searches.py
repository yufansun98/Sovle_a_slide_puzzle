''' 
Structure written by: Nils Napp
Solution by: Jiwon Choi (F18 HW script)
'''
import time
from slideproblem import *
from collections import deque
from queue import PriorityQueue
## you likely need to inport some more modules to do the serach

class Searches:
    def graph_bfs(self, problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        node = Node(None,None,0,problem.initialState)
        if problem.goalTest(node.state):
            return node
        explored = set()
        queue = deque([node])
        while queue:
            node = queue.popleft()
            explored.add(node.state.toTuple())
            for action in problem.applicable(node.state):
                child = child_node(node,action,problem)
                if child.state.toTuple() not in explored and child not in queue:
                    if problem.goalTest(child.state):
                        return solution(child)
                    else:
                         queue.append(child)
        return None

    def recursiveDL_DFS(self, lim, problem):
        n=Node(None,None,0,problem.initialState)
        return self.depthLimitedDFS(n,lim,problem)
        
    def depthLimitedDFS(self, n, lim, problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        if problem.goalTest(n.state):
            return solution(n)
        elif lim == 0:
            return None
        for action in problem.applicable(n.state):
            child = child_node(n, action, problem)
            result = self.depthLimitedDFS(child, lim - 1, problem)
            if result != None:
                return result

        return None



    def id_dfs(self,problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        for depth in range(100):
            result = self.recursiveDL_DFS(depth,problem)
            if result != None:
                return result


    # START: DEFINED ALREADY
    def poseList(self,s):
        poses=list(range(s.boardSize*s.boardSize))
    
        for tile in range(s.boardSize*s.boardSize):
            for row in range(s.boardSize):
                for col in range(s.boardSize):
                    poses[s.board[row][col]]=[row,col]
        return poses
    
    def heuristic(self,s0,sf):
        pl0=self.poseList(s0)
        plf=self.poseList(sf)
    
        h=0
        for i in range(1,s0.boardSize*s0.boardSize):
            h += abs(pl0[i][0] - plf[i][0]) + abs(pl0[i][1] - plf[i][1])
        return h
    # END: DEFINED ALREADY
                
    def a_star_tree(self, problem: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        def get_f(n):
            return n.f
        h = self.heuristic(problem.initialState, problem.goalState)
        node = Node(None, None, 0, problem.initialState)
        node.f = h + node.cost
        frontier = list()
        frontier.append(node)
        while frontier:
            frontier.sort(key=get_f)
            node = frontier.pop(0)
            if problem.goalTest(node.state):
                return solution(node)
            for action in problem.applicable(node.state):
                child = child_node(node, action, problem)
                child.f = self.heuristic(child.state, problem.goalState) + child.cost
                if child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if child.f < frontier[child].f:
                        frontier.remove(child)
                        frontier.append(child)
                        # delet frontier(child) and put child to frontier
        return None

    def a_star_graph(self, problem: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        def get_f(n):
            return n.f
        h = self.heuristic(problem.initialState, problem.goalState)
        node = Node(None, None, 0, problem.initialState)
        node.f = h + node.cost
        frontier = list()
        frontier.append(node)
        explored = set()
        while frontier:
            frontier.sort(key=get_f)
            node = frontier.pop(0)
            if problem.goalTest(node.state):
                return solution(node)
            explored.add(node.state.toTuple())
            for action in problem.applicable(node.state):
                child = child_node(node, action, problem)
                child.f = self.heuristic(child.state, problem.goalState) + child.cost
                if child.state.toTuple() not in explored and child.state.toTuple() not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if child.f < frontier[child].f:
                        frontier.remove(child)
                        frontier.append(child)
        return None

    # EXTRA CREDIT (OPTIONAL)
    def solve4x4(self, p: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        return "Fake return value"

if __name__ == '__main__':
    p=Problem()
    s=State()
    n=Node(None,None, 0, s)
    n2=Node(n,None, 0, s)

    searches = Searches()

    p.goalState=State(s)

    p.apply('R',s)
    p.apply('R',s)
    p.apply('D',s)
    p.apply('D',s)
    p.apply('L',s)

    p.initialState=State(s)


    si=State(s)
    # change the number of random moves appropriately
    # If you are curious see if you get a solution >30 moves. The
    apply_rnd_moves(15,si,p)
    p.initialState=si
    print(p.initialState)
    print(p.goalState)
    # print(searches.poseList(p.goalState))

    startTime=time.perf_counter()


    print('\n\n=== BFS ===\n')
    startTime=time.perf_counter()
    res=searches.graph_bfs(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    # print('\n\n=== depth limited DFS ===\n')
    # startTime=time.perf_counter()
    # res=searches.depthLimitedDFS(Node(None,None,0,p.initialState),10,p)
    # print(time.perf_counter()-startTime)
    # print(Node.nodeCount)
    # print(res)

    print('\n\n=== Iterative Deepening DFS ===\n')
    startTime=time.perf_counter()
    res=searches.id_dfs(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    print('\n\n=== A*-Tree ===\n')
    startTime=time.perf_counter()
    res=searches.a_star_tree(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    print('\n\n=== A*-Graph ===\n')
    startTime=time.perf_counter()
    res=searches.a_star_graph(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    # EXTRA CREDIT (OPTIONAL)
    # UN-COMMENT the code below when you test this
    # change the 'boardSize' variable into 4 from slideproblem.py file
    """
    print('\n\n=== A*-solve4x4 ===\n')
    startTime = time.clock()
    res = searches.solve4x4(p)
    print(time.clock() - startTime)
    print(Node.nodeCount)
    print(res)
    """
