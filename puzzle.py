import main
import time
import random
searcher = main.astar_search


def puzzleManhattan(seed, scrambles):
    problem = main.PuzzleManhattan(4, seed=seed, scrambles=scrambles)
    t1 = time.time()
    solution, counter = searcher(problem)
    t2 = time.time()
    path = solution.path()
    path.reverse()
    print path
    print solution.cammino
    print 'Il tempo necessario per trovare la soluzione ottima con manhattan e: ', t2 - t1, 's'


def puzzleLinearConflict(seed, scrambles):
    problem = main.PuzzleLinearConflict(4, seed=seed, scrambles=scrambles)
    t1 = time.time()
    solution, counter = searcher(problem)
    t2 = time.time()
    path = solution.path()
    path.reverse()
    print path
    print solution.cammino
    print 'Il tempo necessario per trovare la soluzione ottima con linearconflict e: ', t2 - t1, 's'


def puzzleDP(seed, scrambles):
    problem4 = main.PuzzleDP(4, seed=seed, scrambles=scrambles)
    problem4.disjointpattern()
    h = problem4.h(main.Node(problem4.initial))
    print "euristica iniziale: ", h
    t1 = time.time()
    solution, counter = searcher(problem4)
    t2 = time.time()
    path = solution.path()
    path.reverse()
    print path
    print solution.cammino
    print 'Il tempo necessario per trovare la soluzione ottima con DP6-6-3 e: ', t2 - t1, 's'


def puzzleDPreflected(seed, scrambles):
    problem4 = main.PuzzleDPreflected(4, seed=seed, scrambles=scrambles)
    problem4.disjointpattern()
    h = problem4.h(main.Node(problem4.initial))
    print "euristica iniziale: ", h
    t1 = time.time()
    solution, counter = searcher(problem4)
    t2 = time.time()
    path = solution.path()
    path.reverse()
    print path
    print solution.cammino
    print 'Il tempo necessario per trovare la soluzione ottima con DP6-6-3 e: ', t2 - t1, 's'


def testManhattan(number):
    count=0
    seed= random.randint(110, 140)
    print 'seed: ', seed
    scrambles=random.randint(30,50)
    nodeexpanse=0
    t=0
    totalheuristics=0
    print 'scrambles: ',scrambles
    while count<=number:
        count+=1
        print 'iterazione numero: ', count
        problem = main.PuzzleManhattan(4, seed, scrambles)
        h=problem.initial.manhattan()
        print 'euristica iniziale :',h
        totalheuristics += h
        t1 = time.time()
        solution, counter = searcher(problem)
        t2 = time.time()
        print 'Nodi espansi', counter
        nodeexpanse += counter
        print 'Il tempo necessario per trovare la soluzione ottima con Manhattan e: ', t2 - t1, 's'
        t += (t2 -t1)
        print ('  ')
        seed = random.randint(110, 140)
        print 'seed: ', seed
        scrambles = random.randint(30, 50)
        print 'scrambles: ', scrambles
    t /= 100
    print "Valore euristiche: ", totalheuristics
    print "Tempo d'esecuzione medio: ", t
    print "Nodi espansi totali: ", nodeexpanse
    print "Nodi espansi al secondo: ", nodeexpanse/t, "nodi/s"


def testLinearConflict(number):
    count=0
    seed= random.randint(110, 140)
    print 'seed: ', seed
    scrambles=random.randint(30,50)
    nodeexpanse=0
    t=0
    totalheuristics=0
    print 'scrambles: ', scrambles
    while count<=number:
        count+=1
        print 'iterazione numero: ', count
        problem = main.PuzzleLinearConflict(4, seed, scrambles)
        h=problem.initial.lcheuristic()
        print 'euristica iniziale :', h
        totalheuristics += h
        t1 = time.time()
        solution, counter = searcher(problem)
        t2 = time.time()
        print 'Nodi espansi', counter
        nodeexpanse += counter
        print 'Il tempo necessario per trovare la soluzione ottima con Linear Conflict e: ', t2 - t1, 's'
        print ('  ')
        t += (t2 -t1)
        seed = random.randint(110, 140)
        print 'seed: ', seed
        scrambles = random.randint(30, 50)
        print 'scrambles: ', scrambles
    t /= 100
    print "Valore euristiche: ", totalheuristics
    print "Tempo d'esecuzione medio: ", t
    print "Nodi espansi totali: ", nodeexpanse
    print "Nodi espansi al secondo: ", nodeexpanse/t, "nodi/s"


def testDP(number):
    count=0
    seed= random.randint(110, 140)
    print 'seed: ', seed
    scrambles=random.randint(30,50)
    nodeexpanse=0
    t=0
    totalheuristics=0
    print 'scrambles: ', scrambles
    while count<=number:
        count+=1
        print 'iterazione numero: ', count
        problem = main.PuzzleDP(4, seed, scrambles)
        problem.disjointpattern()
        h=problem.h(main.Node(problem.initial))
        print 'euristica iniziale :',h
        totalheuristics += h
        t1 = time.time()
        solution, counter = searcher(problem)
        t2 = time.time()
        print 'Nodi espansi', counter
        nodeexpanse += counter
        print 'Il tempo necessario per trovare la soluzione ottima con Disjoint Pattern 6-6-3 e: ', t2 - t1, 's'
        print ('  ')
        t += (t2 -t1)
        seed = random.randint(110, 140)
        print 'seed: ', seed
        scrambles = random.randint(30, 50)
        print 'scrambles: ', scrambles
    t /= 100
    print "Valore euristiche: ", totalheuristics
    print "Tempo d'esecuzione medio: ", t
    print "Nodi espansi totali: ", nodeexpanse
    print "Nodi espansi al secondo: ", nodeexpanse/t, "nodi/s"


def testDPreflected(number):
    count=0
    seed= random.randint(110, 140)
    print 'seed: ', seed
    scrambles=random.randint(30, 50)
    nodeexpanse=0
    t=0
    totalheuristics=0
    print 'scrambles: ', scrambles
    while count<=number:
        count+=1
        print 'iterazione numero: ', count
        problem = main.PuzzleDPreflected(4, seed, scrambles)
        problem.disjointpattern()
        h=problem.h(main.Node(problem.initial))
        print 'euristica iniziale :', h
        totalheuristics += h
        t1 = time.time()
        solution, counter = searcher(problem)
        t2 = time.time()
        print 'Nodi espansi', counter
        nodeexpanse += counter
        print 'Il tempo necessario per trovare la soluzione ottima con Disjoint Pattern reflected 6-6-3 e: ', t2 - t1, 's'
        print ('  ')
        t += (t2 -t1)
        seed = random.randint(110, 140)
        print 'seed: ', seed
        scrambles = random.randint(30, 50)
        print 'scrambles: ', scrambles
    t /= 100
    print "Valore euristiche: ", totalheuristics
    print "Tempo d'esecuzione medio: ", t
    print "Nodi espansi totali: ", nodeexpanse
    print "Nodi espansi al secondo: ", nodeexpanse/t, "nodi/s"

