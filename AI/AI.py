from random import randint

SIZE_DICT = {
            "small": [8, 8, 10],
            "medium": [16, 16, 40],
            "large": [16, 30, 85]
        }

SURROUNDINGS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

class Logic():
    def __init__(self):
        self.count = 0
        self.cells = set()


class Knowledge_AI():
    def __init__(self, size):
        self.rows, self.columns, self.bombs = SIZE_DICT[size]
        self.start = False
        self.safe = set() # safe to dig
        self.flagged = set()
        self.opened = set()
        self.knowledge = []
        self.k_set = set()

    def get_surroundings(self, row, column):
        surrounding_lst = []
        for x, y in SURROUNDINGS:
            new_row, new_column = row+x, column+y
            if 0 <= new_row < self.rows and 0 <= new_column < self.columns:
                surrounding_lst.append((new_row, new_column))
        return surrounding_lst

    def random_dig(self):
        coords = (randint(0, self.rows-1), randint(0, self.columns-1))
        while coords in self.opened or coords in self.flagged:
            coords = (randint(0, self.rows - 1), randint(0, self.columns - 1))
        return coords

    def update_opened(self, board):
        for x in range(self.rows):
            for y in range(self.columns):
                if board[x][y] != None:
                    self.opened.add((x, y))

    def add_logic(self, board):
        for x in range(self.rows):
            for y in range(self.columns):
                count = board[x][y]

                if count == None or count == 0:
                    continue

                logic = Logic()
                logic.count = count
                s_coords = self.get_surroundings(x, y)

                for c in s_coords:
                    if c in self.flagged:
                        logic.count -= 1
                    elif c not in self.opened and c not in self.safe:
                        logic.cells.add(c)

                if logic.cells:
                    self.knowledge.append(logic)

    def mark_safe(self, coords):
        for i in range(len(self.knowledge)):
            if coords in self.knowledge[i].cells:
                self.knowledge[i].cells.remove(coords)

        self.safe.add(coords)

    def mark_flagged(self, coords):
        for i in range(len(self.knowledge)):
            if coords in self.knowledge[i].cells:
                self.knowledge[i].cells.remove(coords)
                self.knowledge[i].count -= 1

        self.flagged.add(coords)

    def clean_knowledge(self):
        safe = set()
        flagged = set()

        for l in self.knowledge:
            if not l.cells:
                continue
            elif l.count == 0:
                safe.update(l.cells)
            elif l.count == len(l.cells):
                flagged.update(l.cells)

        for s in safe:
            self.mark_safe(s)
        for f in flagged:
            self.mark_flagged(f)

        return safe or flagged

    def update_knowledge(self):
        new_knowledge = []

        for i in range(len(self.knowledge)):
            if not self.knowledge[i].cells:
                continue
            for j in range(len(self.knowledge)):
                if i == j or not self.knowledge[j].cells or self.knowledge[i].cells == self.knowledge[j].cells:
                    continue
                elif self.knowledge[i].cells.issubset(self.knowledge[j].cells):
                    new_logic = Logic()
                    new_logic.cells = self.knowledge[j].cells - self.knowledge[i].cells
                    new_logic.count = self.knowledge[j].count - self.knowledge[i].count
                    new_knowledge.append(new_logic)

        self.knowledge.extend(new_knowledge)

        change = self.clean_knowledge()
        while change:
            change = self.clean_knowledge()

    def play(self, board):
        self.update_opened(board)
        self.add_logic(board)
        self.update_knowledge()

        if not self.start or not self.safe:
            #print("RANDOM!!")
            coords = self.random_dig()
            self.opened.add(coords)
            self.start = True
        else:
            coords = self.safe.pop()
            #print("SAFE: ", coords, self.safe)
        self.opened.add(coords)
        self.knowledge = []
        #print(coords)
        return coords, self.flagged