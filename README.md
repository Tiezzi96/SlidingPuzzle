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

> Alcune classi e funzioni fanno riferimento al codice presente in https://github.com/aimacode e al codice python della lezione tenutasi il giorno 12-10-17, come la classe *Problem*, *Node*, *Puzzle(Problem)* che rispettivamente rappresentano il problema da considerare con il test sull'obiettivo ed il costo del cammino, il nodo che contiene lo stato del problema e verrà utilizzato dalla funzione *astar_search(Problem, h=None)* per eseguire la ricerca su grafo, la classe che realizza l'oggetto **Puzzle** che contiene la funzione *make_initial_state(self,seed, scrambles)*, la quale a partire dallo stato obiettivo esegue un numero random di mosse a seconda del valore di **seed** e **scrambles** generando lo stato iniziale del problema. La classe Puzzle  inoltre, ereditando dalla classe Problem, sovrascrive i metodi *successor* e *goal_test*; definisce inoltre la funzione *h(self, Node)* con valore di ritorno 0. La classe *PuzzleState* viene utilizzata per rappresentare lo stato del problema. Il costruttore riceve in ingresso i valori che costituiscono lo stato del puzzle, oltre a definire righe, colonne e dimensione del puzzle; nel nostro caso il puzzle avra dimensione 4x4 contenente  16 valori da 0 a 15. La funzione *move(self, direction)* viene impiegata per muovere le caselle adiacenti alla posizione vuota a seconda del valore di *direction*. All'interno della classe PuzzleState sono definite sia la funzione *manhattan(self)*, che implementa la funzione euristica che calcola la **distanza di Manhattan**, sia la funzione *lcheuristic(self)* che realizza l'euristica **linear conflict**. Quest'ultima funzione, oltre al valore della distanza di Manhattan, utilizza il valore di ritorno di altre due funzioni, *LCH(self)* e *LCV(self)*, che calcolano i conflitti lineari presenti nello stato corrente del puzzle rispettivamente sulle righe e sulle colonne. Per poter eseguire tale controllo, si ritiene necessario calcolare in precedenza, per ogni casella del puzzle, i conflitti che potenzialmente potrebbero incorrere sia sulle righe che sulle colonne; a tale scopo sono state implementate le funzioni *potlch(self)* e *potlcv(self)*. 

#### A*

> Le funzioni *astar_search(Problem, h=None)*, *best_first_graph_search(problem, f)* e *graph_search(problem, fringe)* costituiscono la strategia di ricerca informata **A\***. Sia la funzione *astar_search* che la funzione *best_first_graph_search* salvano il valore di *h(n)* e *f(n)*, richiamando la funzione *memoize(fn, slot=None)* che salva il valore passato come parametro in una slot precisa, se indicata, o in un dizionario. La funzione *graph_search*, attraverso una ricerca su grafo di tipo BFS, utilizzando come frontiera una lista oridinata in ordine decrescente, ricava lo stato obiettivo del puzzle o estende il nodo corrente aggiungedo i figli alla frontiera. Oltre allo stato obiettivo viene riportato il numero di nodi espansi, che verrà utilizzato durante la fase di test.

#### Tipologie di Puzzle

> Per poter implementare la ricerca **A\*** con le quattro tipologie di euristiche descritte nella relazione è necessario realizzare una diversa implementazione della funzione *h* contenuta nella classe Puzzle. La classi *PuzzleManhattan(Puzzle)*,*PuzzleLinearConflict(Puzzle)*, *PuzzleDP(Puzzle)* e *PuzzleDPreflected(Puzzle)* servono allo scopo.
PuzzleManhattan e PuzzleLinearConflict utilizzano la funzione *manhattan* e la funzione *lcheuristic* per sovrascrivere la funzione *h*. PuzzleDP e PuzzleDPreflected invece per effettuare l'override di *h* devono prima allocare i dizionari realizzati nel file **permutation.py** e salvati su file pickle differenti, uno per ogni gruppo realizzato; tale compito viene svolto dalla funzione *disjoint pattern*. La funzione *h*, dopo aver suddiviso lo stato corrente del nodo nei gruppi del database, controlla se la loro configurazione trova riscontro all'interno dei vari dizionari ed, in caso positivo, estrae il valore dell'euristica. Infine il valore dell'euristica di ogni gruppo viene sommata generando il valore di h per lo stato del puzzle. Le due classi hanno un comportamento analogo salvo per l'utilizzo, da parte di PuzzleDPreflected, di 2 differenti disjoint pattern database e ritorno del valore massimo tra le 2 euristiche generate.  

### Permutation.py
> Il file permutation.py contiene la funzione *permutationstate(N)* utilizzata per realizzare i dizionari necessari per poter utilizzare la ricerca A\* impiegando l'euristica del Disjoint Pattern. La strategia è quella di definire una lista della stessa dimensione di quella impiegata per costruire il puzzle con i valori disposti in ordine crescente ma sostituendo il termine -1 a tutte le caselle che non appartengono al gruppo preso in considerazione. Viene mantenuto il valore della casella vuota a 0. All'interno del file è stata inoltre creata una funzione *move(direction, N, board)*, analoga a quella contenuta nella classe PuzzleState in modo da poter muovere i valori direttamente sulla lista in maniera identica a come si faceva per lo stato. La funzione *permutationstate* partendo quindi dalla lista obiettivo "rilassata", esegue una ricerca su grafo che ha tale lista come radice. Durante la ricerca quindi i nuovi nodi del grafo vengoo salvati nella frontiera mentre i nodi già visitati vengono inseriti nella lista *nodeexpanse*. Alla fine di ogni ciclo i nodi già visitati in precedenza, contenuti nella frontiera, vengono eliminati prima di effettuare l'iterazione successiva. Quando otteniamo una permutazione della lista che ancora non era stata incontrata, tale lista viene inserita in un dizionario avente come chiave la sequenza delle posizioni dei termini del gruppo di caselle preso in considerazione. Quando una lista viene presa in esame per decidere se inserirla o meno nel dizionario solamente le posizioni degli elementi del gruppo in esame vengono prese in considerazione tralasciando sia le coordinate dei -1 sia dello 0. Quando tutte le possibili permutazioni sono state trovate, il ciclo viene interrotto e i dati del dizionario caricati su un apposito file pickle. Per ogni Disjoint Pattern database vengono realizzati 3 file pickle, ovvero 3 differenti dizionari. La tipologia di disjoint pattern utilizzato è 6-6-3 per impossibilità di poter utilizzare la 7-8, dovuta all'improponibile dimensione dei dati da gestire. Per ricercare tutte le possibili configurazioni di un gruppo di 6 caselle è stato necessario un tempo d'esecuzione di 2-3 ore. Per ricercare le configurazioni del gruppo di 3 bastano 1-2 minuti.    

### puzzle.py 
> Il file viene utilizzato per realizzare alcuni test di ricerca, impiegando l'algoritmo A\*, partendo da una particolare configurazione dello stato del puzzle, variando la tipologia di funzione euristica utilizzata. Le funzioni necessarie vengono importate dal file main.py. Dopo aver allocato il Puzzle con un numero arbitrario di *seed* e *scrambles*, si chiama la funzione *astar_search*, passandole il Puzzle come parametro. I valori di ritorno vengono salvati in *solution* e *counter* che solo la soluzione del puzzle e il numero di nodi espansi durante la ricerca. La classe *time* viene utilizzata per conoscere l'istante prima e dopo l'esecuzione della ricerca; la differenza tra i due valori indica il tempo di esecuzione di A\*. Le istruzioni seguenti sono necessarie per calcolare il cammino percorso dalla ricerca sul grafo e visualizzarlo:

    path = solution.path()
    path.reverse()
    print path
    print solution.cammino

> Le funzioni utilizzate per testare un singolo puzzle con differenti euristiche sono: *puzzleManhattan(seed, scrambles)*, *puzzleLinearConflict(seed, scrambles)*, *puzzleDP(seed, scrambles)*, *puzzleDPreflected(seed, scrambles)*. 
I test su 100 casi per tipologia di funzione euristica utilizzata vengono effettuati dalle seguenti funzioni: *testManhattan(number)*, *testLinearCoflict(number)*, *testDP(number)*, *testDPreflected(number)*. Per i test i valori di *seed* e *scrambles* vengono generati randomicamente tra valori compresi tra 110-140 per i seed e 30-50 per gli scrambles; tale limite è imposto per evitare tempi d'esecuzione inaccettabili. Per eseguire ogni test si impiegano cira 2-3 ore.

### test.py
> Il file viene utilizzato per richiamare le funzioni implementate nel file **puzzle.py**. Alcune funzioni sono commentate, quindi al fine di eseguire il programma è sufficiente scegliere la funzione da testare e rimuovere il commento.

## Sitografia
> Per realizzare il progetto sono state consultate le seguenti fonti:
- https://github.com/aimacode
- [Python Code lecture 12-10-2017](http://ai.dinfo.unifi.it/teaching/ai17/search.zip)
- [Korf & Felner(2002)](https://www.sciencedirect.com/science/article/pii/S0004370201000923)
- [Implementing BFS for Pattern Database](https://algorithmsinsight.wordpress.com/graph-theory-2/implementing-bfs-for-pattern-database/)
- [Heuristics for sliding-tile puzzles](https://slideplayer.com/slide/1511516/)

