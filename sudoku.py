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


def SetPosibleNumbers():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0 and type(board[i][j]) is int :
                continue
            board[i][j] = set()
            for trynum in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if not conflict(board, i, j, trynum):
                    board[i][j].add(trynum)


    Removed = 1
    realset = 0
    while Removed:
        logging.info("Original SetPossibleNumbers:\n{}".format(str(board).replace("],", "],\n")))
        Removed = 0
        #find a pair of two-option cells.
        #find 3 numbers in 3 blocks:
        for totalnum in range(2,8):
            for i in range(9):
                for j in range(8):
                    if type(board[i][j]) is set:
                        if len(board[i][j]) == totalnum:
                            Found = 0
                            FoundIndex = [j]
                            for jj in range(9):
                                if jj == j:
                                    continue
                                if type(board[i][jj]) is int:
                                    continue
                                if len(board[i][jj]) <= totalnum:
                                    OtherNumber = False
                                    for x in board[i][jj]:
                                        if x not in board[i][j]:
                                            OtherNumber = True
                                            break
                                    if not OtherNumber:
                                        Found += 1
                                        FoundIndex.append(jj)

                            if Found == totalnum-1:
                                tempremove = 0
                                for jj in range(9):
                                    if type(board[i][jj]) is int:
                                        continue
                                    if jj in FoundIndex:
                                        continue
                                    for x in board[i][j]:
                                        if x in board[i][jj]:
                                            board[i][jj].remove(x)
                                            Removed += 1
                                            tempremove += 1
                                            #logging.info("\t\tRemoved {} from row {},{}".format(x, i, jj))
                                if tempremove > 0:
                                    logging.info("\tIn row {}, found pairs:{} for numbers {}. Removed {}".format(i, FoundIndex, board[i][j], tempremove))

                    if type(board[j][i]) is set:
                        if len(board[j][i]) == totalnum:
                            Found = 0
                            FoundIndex = [j]
                            for jj in range(9):
                                if jj == j:
                                    continue
                                if type(board[jj][i]) is int:
                                    continue
                                if len(board[jj][i]) <= totalnum:
                                    OtherNumber = False
                                    for x in board[jj][i]:
                                        if x not in board[j][i]:
                                            OtherNumber = True
                                            break
                                    if not OtherNumber:
                                        Found += 1
                                        FoundIndex.append(jj)

                            if Found == totalnum-1:
                                tempremove = 0
                                for jj in range(9):
                                    if type(board[jj][i]) is int:
                                        continue
                                    if jj in FoundIndex:
                                        continue
                                    for x in board[j][i]:
                                        if x in board[jj][i]:
                                            board[jj][i].remove(x)
                                            Removed += 1
                                            tempremove += 1
                                            #logging.info("\t\tRemoved {} from col {},{}".format(x, jj, i))
                                if tempremove > 0:
                                    logging.info(
                                        "\tIn col {}, found pairs:{} for numbers {}. Removed {}.".format(i, FoundIndex, board[j][i], tempremove))

            #work on 2-2-2, 3-3-2-2 kind of combination
                cells = []
                numbersincells = set()
                for j in range(9):
                    if type(board[i][j]) is set:
                        if len(board[i][j]) < totalnum:
                            if len(cells) <= totalnum:   #this can be a candidate
                                tempset = set()
                                tempset.update(numbersincells)
                                tempset.update(board[i][j])
                                if len(tempset) > totalnum:
                                    #failed
                                    pass
                                else:
                                    cells.append((i, j))
                                    numbersincells.update(board[i][j])
                                    if len(cells) == totalnum:
                                        break   #found.
                if len(cells) == totalnum:
                    tempremove = 0
                    for j in range(9):
                        if type(board[i][j]) is set:
                            if (i, j) in cells:
                                continue
                            for x in numbersincells:
                                if x in board[i][j]:
                                    board[i][j].remove(x)
                                    Removed += 1
                                    tempremove += 1
                    if tempremove:
                        logging.info(
                            "\tIn row {}, found combination:{} for numbers {}. Removed {}".format(i, cells, numbersincells, tempremove))

                cells = []
                numbersincells = set()
                for j in range(9):
                    if type(board[j][i]) is set:
                        if len(board[j][i]) < totalnum:
                            if len(cells) < totalnum:   #this can be a candidate
                                tempset = set()
                                tempset.update(numbersincells)
                                tempset.update(board[j][i])
                                if len(tempset) > totalnum:
                                    #failed
                                    pass
                                else:
                                    cells.append((j, i))
                                    numbersincells.update(board[j][i])
                                    if len(cells) == totalnum:
                                        break   #found.
                if len(cells) == totalnum:
                    tempremove = 0
                    for j in range(9):
                        if type(board[j][i]) is set:
                            if (j, i) in cells:
                                continue
                            for x in numbersincells:
                                if x in board[j][i]:
                                    board[j][i].remove(x)
                                    Removed += 1
                                    tempremove += 1
                    if tempremove:
                        logging.info(
                            "\tIn column {}, found combination:{} for numbers {}. Removed {}".format(i, cells, numbersincells, tempremove))

            for iloop in range(9):
                iblock = int(iloop / 3)
                jblock = iloop % 3

                for jloop in range(8):
                    i = iblock * 3 + int(jloop/3)
                    j = jblock * 3 + jloop % 3
                    if type(board[i][j]) is set:
                        if len(board[i][j]) == totalnum:
                            Found = 0
                            FoundIndex = [jloop]
                            for nextsequence in range( 9):
                                if nextsequence == jloop:
                                    continue
                                ii = iblock * 3 + int(nextsequence / 3)
                                jj = jblock * 3 + nextsequence % 3
                                if type(board[ii][jj]) is int:
                                    continue
                                if len(board[ii][jj]) <= totalnum:
                                    OtherNumber = False
                                    for x in board[ii][jj]:
                                        if x not in board[i][j]:
                                            OtherNumber = True
                                            break
                                    if not OtherNumber:
                                        Found += 1
                                        FoundIndex.append(nextsequence)
                            if Found == totalnum-1:
                                tempremove = 0
                                for nextsequence in range(9):
                                    ii = iblock * 3 + int(nextsequence / 3)
                                    jj = jblock * 3 + nextsequence % 3
                                    if type(board[ii][jj]) is int:
                                        continue
                                    if nextsequence in FoundIndex:  #ignore the found pair.
                                        continue
                                    for x in board[i][j]:
                                        if x in board[ii][jj]:
                                            board[ii][jj].remove(x)
                                            Removed += 1
                                            tempremove += 1
                                            #logging.info("\t\ttriplet: Removed {} from block {},{}".format(x, ii, jj))
                                if tempremove:
                                    logging.info(
                                        "\tIn block {}/{}, found pairs:{} for numbers {}. Removed {}.".format(iblock, jblock, FoundIndex,
                                                                                             board[i][j], tempremove))

                cells = []
                numbersincells = set()

                for jloop in range(9):

                    i = iblock * 3 + int(jloop / 3)
                    j = jblock * 3 + jloop % 3

                    if type(board[i][j]) is set:
                        if len(board[i][j]) < totalnum:
                            if len(cells) < totalnum:   #this can be a candidate
                                tempset = set()
                                tempset.update(numbersincells)
                                tempset.update(board[i][j])
                                if len(tempset) > totalnum:
                                    #failed
                                    pass
                                else:
                                    cells.append((i, j))
                                    numbersincells.update(board[i][j])
                                    if len(cells) == totalnum:
                                        break   #found.
                if len(cells) == totalnum:
                    tempremove = 0
                    for jloop in range(9):

                        i = iblock * 3 + int(jloop / 3)
                        j = jblock * 3 + jloop % 3

                        if type(board[i][j]) is set:
                            if (i, j) in cells:
                                continue
                            for x in numbersincells:
                                if x in board[i][j]:
                                    board[i][j].remove(x)
                                    Removed += 1
                                    tempremove += 1
                    if tempremove:
                        logging.info(
                            "\tIn block {}/{}, found combination:{} for numbers {}. Removed {}".format(iblock, jblock, cells,
                                                                                           numbersincells, tempremove))

        if Removed:
            logging.info("Removed {} possible numbers".format(Removed))

        realset += SetSingleSetToNumber()

    logging.info("Set {} spaces in SetPosibleNumbers().".format(realset))
    return realset



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

    count += SetPosibleNumbers()

    #logging.info("After SetPossibleNumbers:\n{}".format(str(board).replace("],", "],\n")))
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

    #ResetZero()
    #logging.info("After ResetZero:\n{}".format(str(board).replace("],", "],\n")))

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