import numpy as np
from random import randint

##### INITIATION #####
class Tile():
    def __init__(self):
        self.values_convertion = {
            None: None,
            "M": "M",
            0: ' ',
	    1: '1',
	    2: '2',
	    3: '3',
	    4: '4',
	    5: '5',
	    6: '6',
	    7: '7',
	    8: '8'
        }
        self.value = None
        self.dis_value = self.values_convertion[self.value]
        self.flagged = False
        self.covered = True
        self.scanned = False
        self.r = None
        self.c = None

    def get_value(self):
        return self.value

    def get_dis_value(self):
        return self.dis_value

    def get_flagged(self):
        return self.flagged

    def get_covered(self):
        return self.covered

    def get_scanned(self):
        return self.scanned

    def get_row(self):
        return self.r

    def get_column(self):
        return self.c

    def set_value(self, value):
        self.value = value
        self.dis_value = self.values_convertion[self.value]

    def flag(self):
        self.flagged = True

    def unflag(self):
        self.flag = False

    def uncover(self):
        self.covered = False

    def scan(self):
        self.scanned = True

    def set_row(self, r):
        self.r = r

    def set_column(self, c):
        self.c = c


class Field():
    def __init__(self):
        self.diff_info = {
            'E': [8, 8, 10],
	    'M': [16, 16, 40],
	    'H': [16, 30, 99]
	}
        self.mines_lst = []
        self.untouched = True
        self.explode = False

    def initialise(self):
        print("""
-- Difficulty level --
Easy (E): 8x8, 10 mines
Medium (M): 16x16, 40 mines
Hard (H): 16x30, 99 mines
  """)
        self.diff = input("Enter difficulty level (E/M/H): ")
        while self.diff not in ('E', 'M', 'H'):
            print('invalid input')
            self.diff = input("Enter difficulty level (E/M/H): ")

        self.r = self.diff_info[self.diff][0]
        self.c = self.diff_info[self.diff][1]
        self.mines = self.diff_info[self.diff][2]

        temp_field = []
        for row in range(self.r):
            temp_row = []
            for column in range(self.c):
                temp_tile = Tile()
                temp_tile.set_row(row)
                temp_tile.set_column(column)
                temp_row.append(temp_tile)
            temp_field.append(temp_row)

        self.field = np.array(temp_field)
        return

    def get_row(self):
        return self.r

    def get_column(self):
        return self.c

    def display(self):
        print()
        print("   ", end = "")
        for c_index in range(1, self.c + 1):
            if c_index == self.c:
                print(c_index)
            elif c_index > 9:
                print(c_index, end=" ")
            else:
                print(c_index, end="  ")
        print()
		
        for r_index in range(1, self.r + 1):
            if r_index > 9:
                print(r_index, end=" ")
            else:
                print(r_index, end="  ")
            for c in range(self.c):
                if not self.field[r_index-1, c].get_covered():
                    value = self.field[r_index-1, c].get_dis_value()
                elif self.field[r_index-1, c].get_flagged():
                    value = "F"
                else:
                    value = "?"
                print(value, end = "  ")
                if c == self.c - 1:
                    print("\n")
        print()
        return

    ##### CHECKING METHOD #####
    def display_check(self):
        print("   ", end = "")
        for c_index in range(1, self.c + 1):
            if c_index == self.c:
                print(c_index)
            elif c_index > 9:
                print(c_index, end=" ")
            else:
                print(c_index, end="  ")
		
        for r_index in range(1, self.r + 1):
            if r_index > 9:
                print(r_index, end=" ")
            else:
                print(r_index, end="  ")
            for c in range(self.c):
                value = self.field[r_index-1, c].get_value()
                print(value, end = "  ")
                if c == self.c - 1:
                    print("\n")
        print()
        return
    ##### DELETE LATER #####
    
    def option(self):
        if self.untouched:
            return "D"
        opt = input("Dig/Unflag (D) or Flag (F): ")
        while opt != "D" and opt != "F":
            print("Invalid option")
            opt = input("Dig (D) or Flag/Unflag (F): ")
        return opt
    
    def check_coords_input(self, r, c):
        if not (r.isdigit() and c.isdigit()):
            print("Please enter an integer for each coordinate")
            return False
        r = int(r)
        c = int(c)
        if not((0 < r < self.r) and (0 < c < self.c)):
            print("Please dig within the range of the field")
            return False
        return True

    def check_flag_input(self, r, c):
        if not self.check_coords_input(r, c):
            return False
        r = int(r)-1
        c = int(c)-1
        if not self.field[r, c].get_covered():
            return False
        return True
    
    def make_area_lst(self, r, c):
        area = [r-1, r+2, c-1, c+2]
        for i in range(4):
            if area[i] < 0:
                area[i] = 0
        return self.field[area[0]: area[1], area[2]: area[3]]

    def plant_mines(self, r, c):
        safe_zone = self.make_area_lst(r, c)
        counter = self.mines
        while counter > 0:
            rand_r = randint(0, self.r - 1)
            rand_c = randint(0, self.c - 1)
            if self.field[rand_r, rand_c] in safe_zone:
                continue
            else:
                self.mines_lst.append(self.field[rand_r, rand_c])
                self.field[rand_r, rand_c].set_value("M")
                counter -= 1
        return

    def plant_numbers(self):
        for r in range(self.r):
            for c in range(self.c):
                if self.field[r, c].get_value():
                    continue
                count = 0
                counted_zone = self.make_area_lst(r, c)
                for r2 in counted_zone:
                    for tile in r2:
                        if tile.get_value() == "M":
                            count += 1
                self.field[r, c].set_value(count)
        return
    
    def main_dig(self, r, c):
        if self.untouched:
            self.plant_mines(r, c)
            self.plant_numbers()
            self.untouched = False
        if self.field[r, c].get_covered():
            self.dig_covered(r, c)
        else:
            self.dig_uncovered(r, c)
        return

    def dig_covered(self, r, c):
        self.field[r, c].uncover()
        value = self.field[r, c].get_value()
        scanned = self.field[r, c].get_scanned()
        if value == "M":
            self.explode = True
            self.reveal()
        elif value == 0 and not scanned:
            self.dig_further(r, c)
        return

    def dig_further(self, r, c):
        self.field[r, c].scan()
        scan_zone = self.make_area_lst(r, c)
        for r2 in scan_zone:
            for tile in r2:
                if tile.get_scanned():
                    continue
                else:
                    self.dig_covered(tile.get_row(), tile.get_column())
        return
        
    def dig_uncovered(self, r, c):
        dig_zone = self.make_area_lst(r, c)
        if self.field[r, c].get_value() > self.count_flagged(dig_zone):
            print("Unsafe to dig that tile")
            return
        for r2 in dig_zone:
            for tile in r2:
                if not tile.get_covered() or tile.get_flagged():
                    continue
                else:
                    self.dig_covered(tile.get_row(), tile.get_column())
        return

    def count_flagged(self, zone):
        counter = 0
        for row in zone:
            for tile in row:
                if tile.get_flagged():
                    counter += 1
        return counter
    
    def flag(self, r, c):
        if self.field[r, c].get_flagged():
            self.field[r, c].unflag()
        else:
            self.field[r, c].flag()
        return

    def reveal(self):
        for tile in self.mines_lst:
            tile.uncover()

    def check_end(self):
        return self.explode
    

##### EXECUTION #####
field1 = Field()
field1.initialise()
field1.display()

while not field1.check_end():
    opt = field1.option()
    row = input("Enter row: ")
    column = input("Enter column: ")
    if opt == "D":
        while not field1.check_coords_input(row, column):
            row = input("Enter row: ")
            column = input("Enter column: ")
        field1.main_dig(int(row)-1, int(column)-1)
    elif opt == "F":
        while not field1.check_flag_input(row, column):
            row = input("Enter row: ")
            column = input("Enter column: ")
        field1.flag(int(row)-1, int(column)-1)
    field1.display()
            


