from copy import deepcopy
import psutil
import os
import ast
import cPickle as pickle
import numpy as np


def move(direction, N, board):
    board1 = deepcopy(board)
    row = 0
    col = 0
    for i in range(len(board)):
        if board[i] is 0:
            row = i // N
            col = i % N
            break
    if direction == 'left' and col != 0:
        board1[row * N + col], board1[row * N + col - 1] = board[row * N + col - 1], board[
            row * N + col]
    elif direction == 'right' and col != N - 1:
        board1[row * N + col], board1[row * N + col + 1] = board[row * N + col + 1], board[
            row * N + col]
    elif direction == 'up' and row != 0:
        board1[row * N + col], board1[(row - 1) * N + col] = board[(row - 1) * N + col], board[
            row * N + col]
    elif direction == 'down' and row != N - 1:
        board1[row * N + col], board1[(row + 1) * N + col] = board[(row + 1) * N + col], board[
            row * N + col]
    return board1


def permutationstate(N):
    l = ['up', 'down', 'right', 'left']
    permutation = []
    dictionary = {}
    nodeexpanse = [None] * 58000000
    # nodeexpanse = [None] * 50000
    inizio = []
    list0 = []
    # a = [0, 1, 2, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    # a = [0, -1, -1, -1, 4, 5, -1, -1, 8, 9, -1, -1, 12, 13, -1, -1]
    # a = [0, -1, -1, -1, -1, -1, 6, 7, -1, -1, 10, 11, -1, -1, 14, 15]
    a = [0, -1, -1, -1, -1, -1, -1, -1, -1, 9, 10, 11, -1, 13, 14, 15]
    # a = [0, 1, 2, 3, -1, 5, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1]
    # a = [0, -1, -1, -1, 4, -1, -1, -1, 8, -1, -1, -1, 12, -1, -1, -1]
    inizio.append(a)
    h = 0
    for p in range(N * N):
        # if a[p] is 1 or a[p] is 2 or a[p] is 3:
        # if a[p] is 4 or a[p] is 5 or a[p] is 8 or a[p] is 9 or a[p] is 12 or a[p] is 13:
        # if a[p] is 6 or a[p] is 7 or a[p] is 10 or a[p] is 11 or a[p] is 14 or a[p] is 15:
        # if a[p] is 4 or a[p] is 8 or a[p] is 12:
        # if a[p] is 1 or a[p] is 2 or a[p] is 3 or a[p] is 5 or a[p] is 6 or a[p] is 7:
        if a[p] is 9 or a[p] is 10 or a[p] is 11 or a[p] is 13 or a[p] is 14 or a[p] is 15:
            list1 = []
            list1.append(a[p])
            list1.append(p)
            list0.append(list1)
    inizio.append(h)
    permutation.append(inizio)
    frontier = []
    codiceboard = []
    codiceboard.append(1)
    codiceboard.append(1)
    b=[]
    for i in range(len(list0)):
        e = list0[i][1]
        row = e // N + 1
        codiceboard.append(row)
        b.append(row)
        col = e % N + 1
        codiceboard.append(col)
        b.append(col)
    codiceboard = map(str, codiceboard)
    codiceboard = ''.join(codiceboard)
    codiceboard = int(codiceboard)
    b=map(str, b)
    b=''.join(b)
    b=int(b)
    dictionary[b] = 0
    frontier.append(codiceboard)
    index = 0
    i = 0
    while i <= 90:
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 1024 / 1024
        print("iterazione numero: ", i, "numero permutazioni", len(permutation), "nodi espansi: ", len(nodeexpanse),
              'Memory used (MBytes)', memoryUse)
        board2 = []
        f = []
        print len(frontier)
        while frontier:
            state = frontier.pop()
            nodeexpanse[index] = state
            string = [int(k) for k in str(state)]
            index += 1
            board1 = [-1] * 16
            '''
            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 4
            board1[(string[4] - 1) * N + string[5] - 1] = 5
            board1[(string[6] - 1) * N + string[7] - 1] = 8
            board1[(string[8] - 1) * N + string[9] - 1] = 9
            board1[(string[10] - 1) * N + string[11] - 1] = 12
            board1[(string[12] - 1) * N + string[13] - 1] = 13

            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 6
            board1[(string[4] - 1) * N + string[5] - 1] = 7
            board1[(string[6] - 1) * N + string[7] - 1] = 10
            board1[(string[8] - 1) * N + string[9] - 1] = 11
            board1[(string[10] - 1) * N + string[11] - 1] = 14
            board1[(string[12] - 1) * N + string[13] - 1] = 15
            

            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 4
            board1[(string[4] - 1) * N + string[5] - 1] = 8
            board1[(string[6] - 1) * N + string[7] - 1] = 12
            

            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 1
            board1[(string[4] - 1) * N + string[5] - 1] = 2
            board1[(string[6] - 1) * N + string[7] - 1] = 3
            board1[(string[8] - 1) * N + string[9] - 1] = 5
            board1[(string[10] - 1) * N + string[11] - 1] = 6
            board1[(string[12] - 1) * N + string[13] - 1] = 7
            
            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 1
            board1[(string[4] - 1) * N + string[5] - 1] = 2
            board1[(string[6] - 1) * N + string[7] - 1] = 3
            '''

            board1[(string[0] - 1) * N + string[1] - 1] = 0
            board1[(string[2] - 1) * N + string[3] - 1] = 9
            board1[(string[4] - 1) * N + string[5] - 1] = 10
            board1[(string[6] - 1) * N + string[7] - 1] = 11
            board1[(string[8] - 1) * N + string[9] - 1] = 13
            board1[(string[10] - 1) * N + string[11] - 1] = 14
            board1[(string[12] - 1) * N + string[13] - 1] = 15


            listboard = []
            for d in range(1, 7):
                tmp = []
                position = (string[d * 2] - 1) * N + (string[d * 2 + 1] - 1)
                tmp.append(board1[position])
                tmp.append(position)
                listboard.append(tmp)
            listboard=string[2:]
            listboard = map(str, listboard)
            listboard = ''.join(listboard)
            listboard = int(listboard)
            if listboard in dictionary:
                h = dictionary[listboard]
            for j in range(len(l)):
                h = dictionary[listboard]
                board1_5 = []
                q = l[j]
                board1 = board1
                board = move(l[j], 4, board1)
                list0 = []
                for p in range(N * N):
                    # if board[p] is 1 or board[p] is 2 or board[p] is 3:
                    # if board[p] is 4 or board[p] is 5 or board[p] is 8 or board[p] is 9 or board[p] is 12 or board[p] is 13:
                    # if board[p] is 6 or board[p] is 7 or board[p] is 10 or board[p] is 11 or board[p] is 14 or board[p] is 15:
                    # if board[p] is 4 or board[p] is 8 or board[p] is 12:
                    # if board[p] is 1 or board[p] is 2 or board[p] is 3 or board[p] is 5 or board[p] is 6 or board[p] is 7:
                    if board[p] is 9 or board[p] is 10 or board[p] is 11 or board[p] is 13 or board[p] is 14 or board[p] is 15:
                        list1 = []
                        list1.append(board[p])
                        list1.append(p)
                        list0.append(list1)
                    if len(list0) is 6:
                    # if len(list0) is 3:
                        break
                list0.sort()
                codiceboard = []
                w = 0
                while board[w] != 0:
                    w += 1
                codiceboard.append(w // N + 1)
                codiceboard.append(w % N + 1)
                a=[]
                for k in range(len(list0)):
                    row = list0[k][1] // N + 1
                    codiceboard.append(row)
                    a.append(row)
                    col = list0[k][1] % N + 1
                    codiceboard.append(col)
                    a.append(col)
                codiceboard = map(str, codiceboard)
                codiceboard = ''.join(codiceboard)
                codiceboard = int(codiceboard)
                a = map(str, a)
                a = ''.join(a)
                a = int(a)
                if not a is listboard:
                    h += 1
                if a not in dictionary:
                    board1_5.append(board)
                    board1_5.append(h)
                    board2.append(board1_5)
                    dictionary[a] = h
                if a in dictionary and h < dictionary[a]:
                    dictionary[a]=h
                f.append(codiceboard)
                if len(dictionary) >= 5765760:
                    break
            if len(dictionary) >= 5765760:
                break
        if len(dictionary) >= 5765760:
            # pickle.dump(dictionary, open("DP9-10-11-13-14-15-new.p", "wb"))
            break
        f1 = set(f)
        f1 = f1.difference(set(nodeexpanse))
        f = list(f1)
        f1 = None
        while len(f) is not 0:
            frontier.append(f.pop())
        i += 1

    return permutation, dictionary


solution1, node1 = permutationstate(4)
