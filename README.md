# SlidingPuzzle

## Analisi del Progetto

Il progetto è suddiviso in 4 differenti *Python files*:
- ***main.py***
- ***test.py***
- ***puzzle.py***
- ***permutation.py***

### Main.py
Il file main contiene la maggior parte delle funzioni e classi che costituiscono il progetto.
Alcune classi e funzioni fanno riferimento al codice presente in https://github.com/aimacode, come la classe *problem*, *Node*, *Puzzle(Problem)* che rispettivamente rappresentano il problema da considerare con il test sull'obiettivo ed il costo del cammino, il nodo che contiene lo stato del problema e verrà utilizzato dalla funzione *astar_search(Problem, h=None)* per eseguire la ricerca su grafo, la classe che realizza l'oggetto **Puzzle** che contiene la funzione *make_initial_state(self,seen, scrambles)*, la quale a partire dallo stato obiettivo esegue un numero random di mosse a seconda del valore di **seen** e **scrambles** generando lo stato iniziale del problema. La classe Puzzle  inoltre, ereditando dalla classe Problem, sovrascrive i metodi *successor* e *goal_test*; definisce inoltre la funzione *h(self, Node)* con valore di ritorno 0. La classe *PuzzleState* viene utilizzata per rappresentare lo stato del problema. Il costruttore riceve in ingresso i valori che costituiscono lo stato del puzzle, oltre a definire righe, colonne e dimensione del puzzle; nel nostro caso il puzzle avra dimensione 4\*\4 contenente  16 valori da 0 a 15.


