import sys, logging
board=[]



def loadsudoku(filelocation):
    with open(filelocation, encoding="utf-8") as sudokufile:
            for line in sudokufile:
                if line.startswith("#"):
                    continue    #comment line
                if line.strip():
                    col = line.split(",")
                    column = [int(x.strip()) if x.strip() else 0 for x in col ]
                    board.append(column)


def conflict(b, x, y, digit):
    for i in range(9):
        #col
        if b[x][i] == digit:
            return True
        #row
        if b[i][y] == digit:
            return True

    #block
    xblock = int(x/3)
    yblock = int(y/3)
    for i in range(3):
        for j in range(3):
            if b[xblock*3 + i][yblock*3 + j] == digit:
                return True

    return False


def getnext(x, y):
    x += 1
    if x == 9:
        x = 0
        y += 1
    return x, y


def trysudoku(x, y):
    if not hasattr(trysudoku, "count"):
        trysudoku.count = 0
        trysudoku.failed = 0
    while board[x][y] != 0:
        x, y = getnext(x, y)
        if y == 9:
            return  1   #end!

    for trynum in [1, 2, 3, 4, 5, 6, 7, 8, 9]:   #another function to use [9..1]
#    for trynum in [9, 8, 7, 6, 5, 4, 3, 2, 1]:  # another function to use [9..1]
        if conflict(board, x, y, trynum):
            continue
        trysudoku.count += 1
        board[x][y] = trynum
        nextx, nexty = getnext(x,y)
        if nexty == 9:
            return  1   #end!
        result = trysudoku(nextx, nexty)
        if result == 1:
            return 1
        board[x][y] = 0
        trysudoku.failed += 1
    return -1   #failed after trying all [1..9]



def SetSingleSetToNumber():
    count = 0
    for i in range(9):
        for j in range(9):
            if type(board[i][j]) is set:
                if len(board[i][j]) == 1:
                    board[i][j] = board[i][j].pop()
                    count += 1
    return count


def ResetZero():
    for i in range(9):
        for j in range(9):
            if type(board[i][j]) is set:
                board[i][j] = 0


def preset():
    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                continue
            onlyonefit = 0
            fitnum = 0
            for trynum in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if not conflict(board, i, j, trynum):
                    if onlyonefit == 0:
                        onlyonefit = 1
                        fitnum = trynum
                    else:
                        onlyonefit = 0
                        break   #jump out of trynum
            if onlyonefit == 1:
                board[i][j] = fitnum
                count += 1
    if count > 0:
        logging.info("After initial scan, set {} numbers:\n{}".format(count, str(board).replace("],", "],\n")))

    for i in range(9):
        for trynum in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            possiblesitenum = 0
            possiblesite = 0
            Found = False
            for j in range(9):
                if type(board[i][j]) is int:
                    if board[i][j] == trynum:
                        Found = True
                        break   #found the number.
                else:   #is a set
                    if trynum in board[i][j]:
                        possiblesitenum += 1
                        possiblesite = j

            if Found == False and possiblesitenum == 1:
                logging.info("This num {} can only be in one site {} of this column {}".format(trynum, possiblesite, i))
                board[i][possiblesite] = trynum
                count += 1

            possiblesitenum = 0
            possiblesite = 0
            Found = False
            for j in range(9):
                if type(board[j][i]) is int:
                    if board[j][i] == trynum:
                        Found = True
                        break  # found the number.
                else:  # is a set
                    if trynum in board[j][i]:
                        possiblesitenum += 1
                        possiblesite = j

            if Found == False and possiblesitenum == 1:
                logging.info("This num {} can only be in one site {} of this row {}".format(trynum, possiblesite, i))
                board[possiblesite][i] = trynum
                count += 1

        iblock, jblock = divmod(i, 3)
        for trynum in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            possiblesitenum = 0
            possiblesite = ()
            Found = False
            for j in range(9):
                ii, jj = divmod(j, 3)
                if type(board[iblock*3+ii][jblock*3+jj]) is int:
                    if board[iblock*3+ii][jblock*3+jj] == trynum:
                        Found = True
                        break  # found the number.
                else:  # is a set
                    if trynum in board[iblock*3+ii][jblock*3+jj]:
                        possiblesitenum += 1
                        possiblesite = (iblock*3+ii, jblock*3+jj)

            if Found == False and possiblesitenum == 1:
                logging.info(
                    "This num {} can only be in one site {} in the block".format(trynum, possiblesite))
                board[possiblesite[0]][possiblesite[1]] = trynum
                count += 1

    return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 soduku.py [inputfilename]")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logging.info("Start.")
    loadsudoku(sys.argv[1])
    print("Initial :\n{}".format(str(board).replace("],", "],\n")))
    countinpreset = preset()
    while countinpreset:
        print("Reasoning step: set {} spaces.".format(countinpreset ))
        countinpreset = preset()    #redo until that does not work.

    ResetZero()
    sudokuresult = trysudoku(0, 0)
    if sudokuresult == 1:
        print("Done    :\n{}".format(str(board).replace("],", "],\n")))
        print("\tTried {} times. Failed {} times. Filled {} spaces".format(
            trysudoku.count, trysudoku.failed, trysudoku.count-trysudoku.failed))
    else:
        print("Failed to generate sudoku result after trying {} times!".format(trysudoku.count))

    logging.info("Done")