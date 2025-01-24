import random
from AI import Knowledge_AI
from flask import Flask,  render_template as RT, request

## None: Have not assign a value to the cell
## -1: Bomb
## 0-8: Safe tile with the number indicating the number of bombs around it

SIZE_DICT = {
            "small": [8, 8, 10],
            "medium": [16, 16, 40],
            "large": [16, 30, 85]
        }

SURROUNDINGS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

class Cell():
    def __init__(self):
        self.value = None
        self.uncover = False

class Minesweeper():
    def __init__(self, size):
        self.rows, self.columns, self.bombs = SIZE_DICT[size]
        self.board = [[Cell() for y in range(self.columns)] for x in range(self.rows)]
        self.bomb_lst = []
        self.started = False

    def get_board(self):
        board = []
        for row in self.board:
            temp_row = []
            for cell in row:
                if cell.uncover:
                    temp_row.append(cell.value)
                else:
                    temp_row.append(None)
            board.append(temp_row)
        return board

    def get_uncovered(self):
        uncovered_lst = []
        for x in range(self.rows):
            for y in range(self.columns):
                if self.board[x][y].uncover:
                    uncovered_lst.append((x, y))
        return uncovered_lst


    def get_surroundings(self, row, column):
        surrounding_lst = []
        for x, y in SURROUNDINGS:
            new_row, new_column = row+x, column+y
            if 0 <= new_row < self.rows and 0 <= new_column < self.columns:
                surrounding_lst.append((new_row, new_column))
        return surrounding_lst

    def make_bombs(self, row, column):
        # out-of-bound where bombs cannot be made on these coords
        oob = set(self.get_surroundings(row, column))

        for i in range(self.bombs):
            new_coords = (random.randint(0, self.rows-1), random.randint(0, self.columns - 1))
            if new_coords not in oob and new_coords not in self.bomb_lst:
                self.bomb_lst.append(new_coords)

    def count_bombs(self, row, column):
        count = 0
        s_coords = self.get_surroundings(row, column)
        for coords in s_coords:
            if coords in self.bomb_lst:
                count += 1
        return count

    def set_values(self):
        for x, y in self.bomb_lst:
            self.board[x][y].value = -1

        for x in range(self.rows):
            for y in range(self.columns):
                if not self.board[x][y].value:
                    self.board[x][y].value = self.count_bombs(x, y)


    def initialise(self, row, column):
        # row and column are where the user/AI first clicked to ensure it is not a bomb
        self.make_bombs(row, column)
        self.set_values()

    def dig(self, dig_lst):
        while dig_lst:
            x, y = dig_lst.pop()

            self.board[x][y].uncover = True

            if self.board[x][y].value == 0:
                s_coords = self.get_surroundings(x, y)
                for a, b in s_coords:
                    if not self.board[a][b].uncover and (a, b) not in dig_lst:
                        dig_lst.add((a, b))

    def check_lose(self):
        for row in self.board:
            for cell in row:
                if cell.value == -1 and cell.uncover:
                    return True
        return False

    def check_win(self):
        for row in self.board:
            for cell in row:
                if cell.value > 0 and not cell.uncover:
                    return False
        return True

    def turn(self, row, column):
        if not self.started:
            self.initialise(row, column)
            self.started = True
        self.dig({(row, column)})

        if self.check_lose():
            return -1
        elif self.check_win():
            return 1
        else:
            return 0

def play(size, player, test_random):
    game = Minesweeper(size)

    if player == 1:
        ai = AI(size)
        while True:
            # feed board into AI and get back coords (x, y)
            ai_board = game.get_board()
            coords, flagged = ai.play(ai_board)
            outcome = game.turn(coords[0], coords[1])
            if outcome == 1:
                return True
            elif outcome == -1:
                return False

    else:
        while True:
            x, y = input("enter coords: ").split(" ")
            outcome = game.turn(int(x), int(y))
            if outcome == 1:
                return True
            elif outcome == -1:
                return False

def simulate():
    total = 1000
    counter = 0
    icounter = 0

    print("counting normal")
    for i in range(total):
        win = play("medium", 1, 0)
        if win:
            counter += 1

    print("counting improved")
    for i in range(total):
        win = play("medium", 1, 1)
        if win:
            icounter += 1

    print("Win rate: {}/{}".format(counter, total))
    print("Improved win rate: {}/{}".format(icounter, total))


#simulate()
