import time
import sys
import copy
import os

def fillSets(g, rs, cs, bs):
    # Riempo i set di righe colonne e box
    d = len(g)
    for i in range(d):
        rs.append(set(g[i]))
        cs.append(set([list(colonna) for colonna in zip(*g)][i]))
        bs.append(set())
        for cell in getBoxCells(i):
            bs[i].add(g[cell[0]][cell[1]])

def printGrid(g):
    d = len(g)
    h_line = "-----------------"
    for i in range(d):
        row = ""
        for j in range(d):
            if j%3 == 0:
                if g[i][j] is None:
                    row += "| 0 "
                else:
                    row += "| " + str(g[i][j]) + " "
            else:
                if g[i][j] is not None:
                    row += str(g[i][j]) + " "
                else:
                    row += "0 "
        
        if i%2 == 0:
            print(h_line)
        print(row + "|")
    print(h_line)

def getBoxNumber(i, j):
    return (i // 2)*2 + (j // 3)

def getBoxCells(box):
    cells = []

    box_row = box // 2      # quale fascia verticale
    box_col = box % 2       # quale fascia orizzontale

    start_row = box_row * 2
    start_col = box_col * 3

    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 3):
            cells.append((r, c))

    return cells
	
def checkRow(i, k, rs):       
    return k not in rs[i]

def checkColumn(j, k, cs):
    return k not in cs[j]

def checkBox(b, k, bs):
    return k not in bs[b]

def discardFromAll(i, j, n, rs, cs, bs):
    rs[i].discard(n)
    cs[j].discard(n)
    bs[getBoxNumber(i, j)].discard(n)

def addToAll(i, j, n, rs, cs, bs):
    rs[i].add(n)
    cs[j].add(n)
    bs[getBoxNumber(i, j)].add(n)

# Versione ottimizzata con operazioni insiemistiche
def findMostConstrainedCell(g, rows, columns, boxes):
    dim = len(g)
    min_pns = None
    r, c = -1, -1
    all_digits = {x for x in range(1, dim + 1)}
    for i in range(dim):
        for j in range(dim):
            if g[i][j] is None:
                pns = all_digits - (rows[i] | columns[j] | boxes[getBoxNumber(i, j)])
                # Se trova zero possibilità esce subito
                if len(pns) == 0:
                    return pns, r, c
                # If first empty cell found
                if min_pns is None or len(pns) < len(min_pns):
                    min_pns = pns
                    r, c = i, j

    return min_pns, r, c

def solveGrid(g, check_see_solve, delay = 0.01):
    rows = []
    columns = []
    boxes = []
    d = len(g)
    fillSets(g, rows, columns, boxes)
    if check_see_solve:
        os.system("cls")
        for i in range(d):
            for j in range(d):
                if g[i][j] is not None:
                    sys.stdout.write(f"\033[{i+2};{j+1}H")  
                    sys.stdout.write(str(g[i][j]))
                else:
                    sys.stdout.write(f"\033[{i+2};{j+1}H")
                    sys.stdout.write("0")
        solveWithSetsAndSee(g, rows, columns, boxes, delay)
    else:
        solveWithSets(g, rows, columns, boxes)

def solveWithSets(g, rs, cs, bs):
    min_pns, r, c = findMostConstrainedCell(g, rs, cs, bs)
    if min_pns is None:
        return True
    if len(min_pns) == 0:
        return False
    if len(min_pns) == 1:
        forced = next(iter(min_pns))
        g[r][c] = forced
        addToAll(r, c, forced, rs, cs, bs)
        if solveWithSets(g, rs, cs, bs):
            return True
        g[r][c] = None
        discardFromAll(r, c, forced, rs, cs, bs)
    else:
        for n in min_pns:
            g[r][c] = n
            addToAll(r, c, n, rs, cs, bs)
            if solveWithSets(g, rs, cs, bs):
                return True
            g[r][c] = None   # BACKTRACK
            discardFromAll(r, c, n, rs, cs, bs)
    return False

def solveWithSetsAndSee(g, rs, cs, bs, delay):
    min_pns, r, c = findMostConstrainedCell(g, rs, cs, bs)
    if min_pns is None:
        return True
    if len(min_pns) == 0:
        return False
    if len(min_pns) == 1:
        forced = next(iter(min_pns))
        g[r][c] = forced
        addToAll(r, c, forced, rs, cs, bs)
        sys.stdout.write(f"\033[{r+2};{c+1}H")  # sposta cursore a riga 2, colonna 3
        sys.stdout.write(str(forced))          # scrivi sopra
        sys.stdout.flush()
        time.sleep(delay)
        if solveWithSetsAndSee(g, rs, cs, bs, delay):
            return True
        g[r][c] = None
        discardFromAll(r, c, forced, rs, cs, bs)
        sys.stdout.write(f"\033[{r+2};{c+1}H")  # sposta cursore a riga 2, colonna 3
        sys.stdout.write("0")          # scrivi sopra
        sys.stdout.flush()
        time.sleep(delay)
    else:
        for n in min_pns:
            g[r][c] = n
            addToAll(r, c, n, rs, cs, bs)
            sys.stdout.write(f"\033[{r+2};{c+1}H")  # sposta cursore a riga 2, colonna 3
            sys.stdout.write(str(n))          # scrivi sopra
            sys.stdout.flush()
            time.sleep(delay)
            if solveWithSetsAndSee(g, rs, cs, bs, delay):
                return True
            g[r][c] = None   # BACKTRACK
            discardFromAll(r, c, n, rs, cs, bs)
            sys.stdout.write(f"\033[{r+2};{c+1}H")  # sposta cursore a riga 2, colonna 3
            sys.stdout.write("0")          # scrivi sopra
            sys.stdout.flush()
            time.sleep(delay)
    return False

if __name__ == "__main__":

#     # Variabili globali
#     grid = [
#     [5, None, None, 4, None, None, None, None, None],
#     [None, None, None, None, 9, 3, None, None, 8],
#     [None, 7, None, None, None, None, None, 1, None],
#     [None, 6, None, 1, None, 9, None, None, None],
#     [None, None, None, None, None, None, 7, 3, None],
#     [None, None, 2, 6, None, None, None, None, None],
#     [None, 9, None, None, 8, None, 4, None, 7],
#     [None, 2, 3, None, None, None, None, 9, None],
#     [None, 5, None, None, None, 4, None, None, None]
#     ]

#     initial_grid = copy.deepcopy(grid)

#     # Dimensione griglia
#     d = len(grid)
#     N = 1000

#     start = time.time()

#     for _ in range(N):
#         grid = copy.deepcopy(initial_grid)
#         solveGrid(grid, False)

#     print(f"Runtime medio su {N} solves: {(time.time()-start)/N}")
#     print("Initial grid:")
#     printGrid(initial_grid)
#     print("\n")
#     print("Solved grid:")
#     printGrid(grid)
    print(getBoxCells(5))