# SlidingPuzzle

## Analisi del Progetto

Il progetto è suddiviso in 4 differenti *Python files*:
- ***main.py***
- ***test.py***
- ***puzzle.py***
- ***permutation.py***

### Main.py

> Il file main contiene la maggior parte delle funzioni e classi che costituiscono il progetto.

#### Il Puzzle

Alcune classi e funzioni fanno riferimento al codice presente in https://github.com/aimacode, come la classe *problem*, *Node*, 
*Puzzle(Problem)* che rispettivamente rappresentano il problema da considerare con il test sull'obiettivo ed il costo del cammino, il nodo che contiene lo stato del problema e verrà utilizzato dalla funzione *astar_search(Problem, h=None)* per eseguire la ricerca su grafo, la classe che realizza l'oggetto **Puzzle** che contiene la funzione *make_initial_state(self,seen, scrambles)*, la quale a partire dallo stato obiettivo esegue un numero random di mosse a seconda del valore di **seen** e **scrambles** generando lo stato iniziale del problema. La classe Puzzle  inoltre, ereditando dalla classe Problem, sovrascrive i metodi *successor* e *goal_test*; definisce inoltre la funzione *h(self, Node)* con valore di ritorno 0. La classe *PuzzleState* viene utilizzata per rappresentare lo stato del problema. Il costruttore riceve in ingresso i valori che costituiscono lo stato del puzzle, oltre a definire righe, colonne e dimensione del puzzle; nel nostro caso il puzzle avra dimensione 4x4 contenente  16 valori da 0 a 15. La finzione *move(self, direction)* viene impiegata per muovere le caselle adiacenti alla posizione vuota a seconda del valore di *direction*. All'interno della classe PuzzleState sono definite sia la funzione *manhattan(self)*, che 
implementa la funzione euristica che calcola la **distanza di Manhattan**, sia la funzione *lcheuristic(self)* che realizza la 
l'euristica **linear conflict**. Quest'ultima funzione, oltre al valore della distanza di Manhattan, utilizza il valore di ritorno di altre due funzioni, *LCH(self)* e *LCV(self)*, che calcolano i conflitti lineari presenti nello stato corrente del puzzle rispettivamente sulle righe e sulle colonne. Per poter eseguire tale controllo, si ritiene necessario calcolare in precedenza, per ogni casella del puzzle, i conflitti che potenzialmente potrebbero incorrere sia sulle righe che sulle colonne; a tale scopo sono state implementate le funzioni *potlch(self)* e *potlcv(self)*. 






