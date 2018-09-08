
from __future__ import print_function
from __future__ import generators

import sys
import time
import os
import psutil
from copy import deepcopy
import random
import bisect
import pickle
infinity = 1.0e400


def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


class Problem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        pass # abstract

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        update(self, state=state, parent=parent, action=action,
               path_cost=path_cost, depth=0)
        if parent:
            self.depth = parent.depth + 1
        self.cammino=0
        self.camminoimp=0

    def __repr__(self):
        """(pf) Modified to display depth, f and h"""
        if hasattr(self,'f'):
            return "<Node: f=%d, depth=%d, h=%d\n%s>" % (self.f,
                                                         self.depth,
                                                         self.h,
                                                         self.state)
        else:
            return "<Node: depth=%d\n%s>" % (self.depth,self.state)

    def path(self):
        "Create a list of nodes from the root to this node."
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
            self.cammino+=1
            self.camminoimp+=x.state.hu
        return result

    def expand(self, problem):
        "Return a list of nodes reachable from this node. [Fig. 3.8]"
        return [Node(next_state, self, action,
                     problem.path_cost(self.path_cost, self.state, action, next_state))
                for (action, next_state) in problem.successor(self.state)]


class PuzzleState:
    """
    The board is NxN so use N=4 for the 15-puzzle, N=5 for
    the 24-puzzle, etc
    The state of the puzzle is simply a permutation of 0..N-1
    The position of the blank (element zero) is stored in r,c
    """
    def __init__(self,board,N,r,c):
        self.board=board
        self.r=r
        self.c=c
        self.N = N
        self.hu = 0

    def __getitem__(self,(r,c)):
        return self.board[r*self.N+c]

    def __setitem__(self,(r,c),val):
        self.board[r*self.N+c]=val

    def move(self,direction):
        ch=deepcopy(self)
        c,r = ch.c,ch.r

        if direction == 'left' and self.c != 0:
            ch[(r,c)], ch[(r,c-1)] = self[(r,c-1)],self[(r,c)]
            ch.c = c-1
        elif direction == 'right' and c != self.N-1:
            ch[(r,c)],ch[(r,c+1)] = self[(r,c+1)],self[(r,c)]
            ch.c = c+1
        elif direction == 'up' and self.r != 0:
            ch[(r,c)],ch[(r-1,c)] = self[(r-1,c)],self[(r,c)]
            ch.r = r-1
        elif direction == 'down' and r != self.N-1:
            ch[(r,c)],ch[(r+1,c)] = self[(r+1,c)],self[(r,c)]
            ch.r = r+1
        else:
            return None
        return ch

    def misplaced(self):
        """Misplaced tiles heuristic"""
        blank = self.r*self.N+self.c
        return sum([idx!=val for idx,val in enumerate(self.board) if idx!=blank])

    def lcheuristic(self):
        m = self.manhattan()
        m += self.LCH()
        m += (self.LCV())
        return m

    def potlch(self):
        a = range(16)
        listup = []
        listdown = []
        for j in range(self.N):
            for i in range(self.N):
                l = []
                l1 = []
                d = i
                u = i
                while u != 3:
                    u += 1
                    if a[j * self.N + u] is not 0:
                        l.append(a[j * self.N + u])

                while d != 0:
                    d -= 1
                    if a[j * self.N + d] is not 0:
                        l1.append(a[j * self.N + d])
                listup.append(l)
                listdown.append(l1)
        return (listup, listdown)

    def potlcv(self):
        a = range(16)
        listup = []
        listdown = []
        for i in range(self.N):
            for j in range(self.N):
                l = []
                l1 = []
                d = j
                u = j
                while u != 3:
                    u += 1
                    if a[u * self.N + i] is not 0:
                        l.append(a[u * self.N + i])

                while d != 0:
                    d -= 1
                    if a[d * self.N + i] is not 0:
                        l1.append(a[d * self.N + i])
                listup.append(l)
                listdown.append(l1)
        return (listup, listdown)

    def LCH(self):
        linearconflict = 0
        listup, listdown = self.potlch()
        for j in range(self.N):
            for i in range(self.N):
                if self[(j,i)] != 0:
                    k=i
                    u=i
                    casella=self[[j,i]]
                    while k != 3:
                        k += 1
                        for l in range(len(listdown[self[(j,i)]])):
                            if self[(j,k)]==listdown[self[(j,i)]][l] and j is (self[(j,i)]//4):
                                linearconflict+=1
                    while u != 0:
                        u -= 1
                        for l in range(len(listup[self[(j,i)]])):
                            if self[(j, u)] == listup[self[(j,i)]][l] and j is (self[(j,i)]//4):
                                linearconflict += 1
        return linearconflict

    def LCV(self):
        linearconflict = 0
        listup, listdown = self.potlcv()
        for j in range(self.N):
            for i in range(self.N):
                if self[(i,j)] != 0:
                    k=i
                    u=i
                    a=range(16)
                    col=-1
                    row=-1
                    for n in range(self.N):
                        for m in range(self.N):
                            if a[m*self.N+n] is self[(i,j)]:
                                col=n
                                row=m
                    while k != 3:
                        k += 1
                        for l in range(len(listdown[col*self.N +row])):
                            if self[(k,j)]==listdown[col*self.N +row][l] and j is (self[(i,j)] % 4):
                                linearconflict+=1
                    while u != 0:
                        u -= 1
                        for l in range(len(listup[col*self.N +row])):
                            if self[(u, j)] == listup[col*self.N +row][l] and j is (self[(i,j)] % 4):
                                linearconflict += 1
        return linearconflict

    def manhattan(self):
        """Manhattan distance heuristic"""
        m=0
        blank = self.r*self.N+self.c
        for index,value in enumerate(self.board):
            if index != blank and index != value:
                r = index // self.N
                c = index % self.N
                rr = value // self.N
                cc = value % self.N
                # print('misplaced',value,rr,r,cc,c)
                m += abs(r-rr) + abs(c-cc)
        assert(m>=0)
        return m

    def __str__(self): # forza un dato ad essere una stringa
        """Serialize the state in a human-readable form"""
        s = ''
        for r in xrange(self.N):
            for c in xrange(self.N):
                if self[(r,c)]>0:
                    s += '%3d' % self[(r,c)]
                else:
                    s += '   '
            s += '\n'
        return s

    def __repr__(self):
        return self.__str__()


class Puzzle(Problem):
    """Base class - For 8-puzzle use Puzzle(3) -- a 3x3 grid"""
    def __init__(self, N, seed,scrambles=10):
        self.N = N
        self.actions = ['left','right','up','down']
        self.make_initial_state(seed,scrambles)
        self.dict1 = {}
        self.dict2 = {}
        self.dict3 = {}
        self.dict4 = {}
        self.dict5 = {}
        self.dict6 = {}

    def make_initial_state(self,seed,scrambles):
        """
        To ensure a solution exists, start from the goal and scramble
        it applying a random sequence of actions. An alternative is to
        use the permutation parity property of the puzzle but using
        the scrambling we can roughly control the depth of the
        solution and thus limit CPU time for demonstration
        """
        seen = {}
        ns=0
        x = range(self.N*self.N)

        for r in range(self.N):
            for c in range(self.N):
                if x[r*self.N+c]==0:
                    row,col=r,c
        self.initial = PuzzleState(x,self.N,row,col)
        R = random.Random()
        R.seed(seed)
        while ns<scrambles:
            index = R.randint(0,len(self.actions)-1)
            a = self.actions[index]
            nexts = self.initial.move(a)
            if nexts is not None:
                serial = nexts.__str__()
                if serial not in seen:
                    seen[serial] = True
                    self.initial = nexts
                    ns += 1
        print('Problem:', self.__doc__, 'Initial state:')
        print(self.initial)
        print('==============')

    def successor(self, state):
        """Legal moves (blank moves left, right, up,
        down). Implemented as a generator"""
        for action in self.actions:
            nexts = state.move(action)
            if nexts is not None:
                yield (action,nexts)

    def goal_test(self, state):
        """For simplicity blank on top left"""
        return state.board==range(self.N*self.N)

    def h(self,node):
        """No heuristic. A* becomes uniform cost in this case"""
        return 0


def graph_search(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one. [Fig. 3.18]"""
    counter = 0
    closed = {}
    fringe.append(Node(problem.initial))
    max_depth=0
    while fringe:
        node = fringe.pop()
        # Print some information about search progress
        if node.depth>max_depth:
            max_depth=node.depth
            if max_depth<50 or max_depth % 1000 == 0:
                pid = os.getpid()
                py = psutil.Process(pid)
                memoryUse = py.memory_info()[0]/1024/1024
                print('Reached depth',max_depth,
                      'Open len', len(fringe),
                      'Node expanse', counter,
                      'Memory used (MBytes)', memoryUse)

        if problem.goal_test(node.state):
            return node, counter
        serial = node.state.__str__()
        if serial not in closed:
            counter += 1
            closed[serial] = True
            fringe.extend(node.expand(problem))
    return None


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    return graph_search(problem, PriorityQueue(min, f))


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search.
    Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n))."""
    h = h or problem.h
    h = memoize(h, 'h')

    def f(n):
        return max(getattr(n, 'f', -infinity), n.path_cost + h(n))
    return best_first_graph_search(problem, f)


def memoize(fn, slot=None):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, store results in a dictionary."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if not memoized_fn.cache.has_key(args):
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]

        memoized_fn.cache = {}
    return memoized_fn


class Queue:
    """Queue is an abstract class/interface. There are three types:
        Stack(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(lt): Queue where items are sorted by lt, (default <).
    Each type supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
    Note that isinstance(Stack(), Queue) is false, because we implement stacks
    as lists.  If Python ever gets interfaces, Queue will be an interface."""

    def __init__(self):
        abstract

    def extend(self, items):
        for item in items: self.append(item)


class PriorityQueue(Queue):
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x)."""

    def __init__(self, order=min, f=lambda x: x):
        update(self, A=[], order=order, f=f)

    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def __len__(self):
        return len(self.A)

    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        elif self.order is max:
            return self.A.pop(len(self.A)-1)[1]
        else:
            return self.A.pop()[1]

    def fmin(self):
        return self.A[0][0]


class PuzzleManhattan(Puzzle):
    """Manhattan heuristic"""
    def h(self, node):
        return node.state.manhattan()


class PuzzleLinearConflict(Puzzle):
    def h(self, node):
        return node.state.lcheuristic()


class PuzzleDPreflected(Puzzle):
    def disjointpattern(self):
        dict1=pickle.load(open('DP1-2-3-new.p', 'rb'))
        print('scaricato file DP1-2-3-new.p: ', len(dict1))
        dict2 = pickle.load(open('DP4-5-8-9-12-13-new.p', 'rb'))
        print('scaricato file DP4-5-8-12-13-new.p: ', len(dict2))
        dict3 = pickle.load(open('DP6-7-10-11-14-15-new.p', 'rb'))
        print('scaricato file DP6-7-10-11-14-15-new.p: ', len(dict3))
        dict4 = pickle.load(open('DP4-8-12-new.p', 'rb'))
        print('scaricato file DP4-8-12-new.p: ', len(dict4))
        dict5 = pickle.load(open('DP1-2-3-5-6-7-new.p', 'rb'))
        print('scaricato file DP1-2-3-5-6-7-new.p: ', len(dict5))
        dict6 = pickle.load(open('DP9-10-11-13-14-15-new.p', 'rb'))
        print('scaricato file DP9-10-11-13-14-15-new.p: ', len(dict6))
        self.dict1 = dict1
        self.dict2 = dict2
        self.dict3 = dict3
        self.dict4 = dict4
        self.dict5 = dict5
        self.dict6 = dict6

    def h(self, node):
        board = node.state.board
        board1 = []
        board2 = []
        board3 = []
        board4 = []
        board5 = []
        board6 = []
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        for p in range(len(board)):
            if board[p] is 1 or board[p] is 2 or board[p] is 3:
                list = []
                list.append(board[p])
                list.append(p)
                list1.append(list)
            if board[p] is 4 or board[p] is 5 or board[p] is 8 or board[p] is 9 or board[p] is 12 or board[p] is 13:
                list = []
                list.append(board[p])
                list.append(p)
                list2.append(list)
            if board[p] is 6 or board[p] is 7 or board[p] is 10 or board[p] is 11 or board[p] is 14 or board[p] is 15:
                list = []
                list.append(board[p])
                list.append(p)
                list3.append(list)
            if board[p] is 4 or board[p] is 8 or board[p] is 12:
                list = []
                list.append(board[p])
                list.append(p)
                list4.append(list)
            if board[p] is 1 or board[p] is 2 or board[p] is 3 or board[p] is 5 or board[p] is 6 or board[p] is 7:
                list = []
                list.append(board[p])
                list.append(p)
                list5.append(list)
            if board[p] is 9 or board[p] is 10 or board[p] is 11 or board[p] is 13 or board[p] is 14 or board[p] is 15:
                list = []
                list.append(board[p])
                list.append(p)
                list6.append(list)
        list1.sort()
        list2.sort()
        list3.sort()
        list4.sort()
        list5.sort()
        list6.sort()
        for p in range(len(list1)):
            e = list1[p][1]
            e1 = list4[p][1]
            row = e // 4 + 1
            row1 = e1 // 4 + 1
            board1.append(row)
            board4.append(row1)
            col = e % 4 + 1
            col1 = e1 % 4 + 1
            board1.append(col)
            board4.append(col1)
        for p in range(len(list2)):
            e = list2[p][1]
            e1= list3[p][1]
            e2 = list5[p][1]
            e3 = list6[p][1]
            row = e // 4 + 1
            row1 = e1 // 4 + 1
            row2 = e2 // 4 + 1
            row3 = e3 // 4 + 1
            board2.append(row)
            board3.append(row1)
            board5.append(row2)
            board6.append(row3)
            col = e % 4 + 1
            col1 = e1 % 4 + 1
            col2 = e2 % 4 + 1
            col3 = e3 % 4 + 1
            board2.append(col)
            board3.append(col1)
            board5.append(col2)
            board6.append(col3)

        board1 = map(str,board1)
        board1 = ''.join(board1)
        board1 = int(board1)

        board2 = map(str, board2)
        board2 = ''.join(board2)
        board2 = int(board2)

        board3 = map(str, board3)
        board3 = ''.join(board3)
        board3 = int(board3)

        board4 = map(str, board4)
        board4 = ''.join(board4)
        board4 = int(board4)

        board5 = map(str, board5)
        board5 = ''.join(board5)
        board5 = int(board5)

        board6 = map(str, board6)
        board6 = ''.join(board6)
        board6 = int(board6)

        h1 = self.dict1[board1]
        h2 = self.dict2[board2]
        h3 = self.dict3[board3]
        h4 = self.dict4[board4]
        h5 = self.dict5[board5]
        h6 = self.dict6[board6]

        hfirst = h1+h2+h3
        hsecond = h4+h5+h6

        h = max(hfirst, hsecond)
        return h


class PuzzleDP(Puzzle):

    def disjointpattern(self):
        dict1 = pickle.load(open('DP1-2-3-new.p', 'rb'))
        print('scaricato file DP1-2-3-new.p: ', len(dict1))
        dict2 = pickle.load(open('DP4-5-8-9-12-13-new.p', 'rb'))
        print('scaricato file DP4-5-8-9-12-13-new.p: ', len(dict2))
        dict3 = pickle.load(open('DP6-7-10-11-14-15-new.p', 'rb'))
        print('scaricato file DP6-7-10-11-14-15-new.p: ', len(dict3))
        self.dict1 = dict1
        self.dict2 = dict2
        self.dict3 = dict3

    def h(self, node):
        board = node.state.board
        board1 = []
        board2 = []
        board3 = []
        list1=[]
        list2= []
        list3 = []

        for p in range(len(board)):
            if board[p] is 1 or board[p] is 2 or board[p] is 3:
                list = []
                list.append(board[p])
                list.append(p)
                list1.append(list)
            if board[p] is 4 or board[p] is 5 or board[p] is 8 or board[p] is 9 or board[p] is 12 or board[p] is 13:
                list = []
                list.append(board[p])
                list.append(p)
                list2.append(list)
            if board[p] is 6 or board[p] is 7 or board[p] is 10 or board[p] is 11 or board[p] is 14 or board[p] is 15:
                list = []
                list.append(board[p])
                list.append(p)
                list3.append(list)
        list1.sort()
        list2.sort()
        list3.sort()
        for p in range(len(list1)):
            e = list1[p][1]
            row = e // 4 + 1
            board1.append(row)
            col = e % 4 + 1
            board1.append(col)
        for p in range(len(list2)):
            e = list2[p][1]
            e1= list3[p][1]
            row = e // 4 + 1
            row1 = e1 // 4 + 1
            board2.append(row)
            board3.append(row1)
            col = e % 4 + 1
            col1 = e1 % 4 + 1
            board2.append(col)
            board3.append(col1)

        board1 = map(str,board1)
        board1 = ''.join(board1)
        board1 = int(board1)

        board2 = map(str, board2)
        board2 = ''.join(board2)
        board2 = int(board2)

        board3 = map(str, board3)
        board3 = ''.join(board3)
        board3 = int(board3)

        h1 = self.dict1[board1]
        h2 = self.dict2[board2]
        h3 = self.dict3[board3]

        h = h1+h2+h3
        return h






