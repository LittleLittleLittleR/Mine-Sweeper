#MINESWEEPER
import random
uncovered_tiles = []
def prnt(board):
    """prints the board"""
    for column in range(len(board)):
        if column == 0:
            print("   {}".format(column), end = "  ")
        elif column == len(board)-1:    
            print(column)
        elif len(str(column)) == 1:
            print(column, end = "  ")
        elif len(str(column)) == 2:
            print(column, end = " ")
    for a in range(len(board)):
        if len(str(a)) == 1:
            print(a, end = "  ")
        elif len(str(a)) == 2:
            print(a, end = " ")
        for b in range(len(board)):
            if b == len(board)-1:
                print(board[a][b])
            else:
                print(board[a][b], end = "  ")
    print("")

def difficulty():
    """Sets the difficulty of the minesweeper game"""
    d = input("Please enter the difficulty -> easy(e), medium(m), hard(h): ")
    print("")
    while not(d in ["e", "m", "h"]):
        print("Invald input")
        d = input("Please enter the difficulty -> easy(e), medium(m), hard(h): ")
        print("")
    if d == "e":
        return [9, 10]
    elif d == "m":
        return [16, 40]
    elif d == "h":
        return [25, 100]

def find_number(exposed, coords):
    """Finds the number that should show on a certain tile on the board"""
    l = ((coords[0]+1, coords[1]),(coords[0]-1, coords[1]),(coords[0], coords[1]+1),(coords[0], coords[1]-1),(coords[0]+1, coords[1]+1),(coords[0]-1, coords[1]+1),(coords[0]+1, coords[1]-1),(coords[0]-1, coords[1]-1))
    count = 0
    for x in l:
        if not(x[0] in range(len(exposed))) or not(x[1] in range(len(exposed))):
            continue
        if exposed[x[0]][x[1]] == "B":
            count += 1
    return count

def createmines(board, b):
    """Creates the mines and randomly puts them in the exposed board"""
    mlist = []
    for x in range(b):
        mine = [random.randrange(len(board)), random.randrange(len(board))]
        while mine in mlist:
            mine = [random.randrange(len(board)), random.randrange(len(board))]
        board[mine[0]][mine[1]] = "B"
        mlist.append(mine)
    return board

def createboards(l): #Input should be a list with 2 elements, [board length, mines]
    """Creates 2 boards, board that has its elements hidden and an exposed board"""
    covered = []
    exposed = []
    for b in range(l[0]):
        covered.append([" "]*l[0])
        exposed.append([" "]*l[0])
    exposed = createmines(exposed, l[1])
    for c in range(len(exposed)):
        for d in range(len(exposed[c])):
            if exposed[c][d] != "B":
                exposed[c][d] = find_number(exposed, [c, d])
    return [exposed, covered]


#INTERACTION WITH PLAYER BELOW
def coordcheck(board, coords):
    for i in coords:
        if not(i.isdigit()):
            return False
        if not(int(i) in range(len(board))):
            return False
    return True


def flag(covered):
    y = input("Enter row number to flag: ")
    x = input("Enter column number to flag: ")
    print("")
    while not(coordcheck(covered, [y, x])):
        print("Invalid input")
        y = input("Enter row number to flag: ")
        x = input("Enter column number to flag: ")
        print("")
    else:
        x, y = int(x), int(y)
    if covered[y][x] == "F":
        covered[y][x] = " "
    elif covered[y][x] != " ":
        print("You cannot flag this tile")
        print("")
    else:
        covered[y][x] = "F"
    return covered

def ggwp(boards):
    for y in range(len(boards[0])):
        for x in range(len(boards[0][y])):
            if boards[0][y][x] == "B":
                boards[1][y][x] = "B"
    return boards
    
def dig_area(boards, coords):
    global uncovered_tiles
    l = [coords]
    potential_neighbours = ((coords[0]+1, coords[1]),(coords[0]-1, coords[1]),(coords[0], coords[1]+1),(coords[0], coords[1]-1),(coords[0]+1, coords[1]+1),(coords[0]-1, coords[1]+1),(coords[0]+1, coords[1]-1),(coords[0]-1, coords[1]-1))
    real_neighbours = []
    for a in potential_neighbours:
        if not(a[0] in range(len(boards[0]))) or not(a[1] in range(len(boards[0]))) or a in uncovered_tiles:
            continue
        if boards[0][a[0]][a[1]] == "B":
            return l
        real_neighbours.append(a)
    for b in real_neighbours:
        uncovered_tiles.append(b)
        l += dig_area(boards, b)
    return l
        
def force_dig(boards, coords):
    global uncovered_tiles
    l = [coords]
    potential_neighbours = ((coords[0]+1, coords[1]),(coords[0]-1, coords[1]),(coords[0], coords[1]+1),(coords[0], coords[1]-1),(coords[0]+1, coords[1]+1),(coords[0]-1, coords[1]+1),(coords[0]+1, coords[1]-1),(coords[0]-1, coords[1]-1))
    for a in potential_neighbours:
        if not(a[0] in range(len(boards[0]))) or not(a[1] in range(len(boards[0]))):
            continue
        if a in uncovered_tiles:
            continue
        if boards[1][a[0]][a[1]] == "F":
            continue
        l.append(a)
    return l
            
    
def dig(boards, coords):
    if boards[1][coords[0]][coords[1]] == "F":
        print("Cannot dig up flag!")
        print("")
        return boards
    if boards[0][coords[0]][coords[1]] == "B":
        boards[1][coords[0]][coords[1]] = "B"
        return boards
    if boards[1][coords[0]][coords[1]] == " ":
        l = dig_area(boards, coords)
    else:
        l = force_dig(boards, coords)
    for i in l:
        boards[1][i[0]][i[1]] = boards[0][i[0]][i[1]]
    return boards
    
def enter(boards):
    tool = input("Do you want to flag(f) or dig(d): ")
    print("")
    while not(tool in ["f", "d"]):
        print("Invalid input")
        tool = input("Do you want to flag(f) or dig(d): ")
        print("")
    if tool == "f":
        boards[1] =  flag(boards[1])
    else:
        y = input("Enter row number to dig: ")
        x = input("Enter column number to dig: ")
        print("")
        while not(coordcheck(boards[1], [y, x])):
            print("Invalid input")
            y = input("Enter row number to dig: ")
            x = input("Enter column number to dig: ")
            print("")
        else:
            x, y = int(x), int(y)
        boards = dig(boards, (y, x))
    return boards

boards = createboards(difficulty())
while (True in [" " in i for i in boards[1]]) and all([not("B" in j) for j in boards[1]]):
    prnt(boards[1])
    boards = enter(boards)
if not(all([not("B" in j) for j in boards[1]])):
    boards = ggwp(boards)
    prnt(boards[1])
    print("You Lose!")
else:
    prnt(boards[1])
    print("You Win!")
