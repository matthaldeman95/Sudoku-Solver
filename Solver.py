import numpy as np
class Grid:
    """
    Class for the Sudoku puzzle grid.  grid contains the puzzle with zeroes in place of
    blank spaces.  boolgrid maps all nonzero values to one and zeroes to zero,
    for the purpose of preventing the initial values of the puzzle from being modified
    """
    def __init__(self, grid):
        self.grid = grid
        self.boolgrid = np.matrix(grid.astype(bool))

    def genSquare(self, row, col):
        """
        Generates the 3x3 square a given cell is a part of, for
            checking whether a value can belong to that cell
        :param row: row of square
        :param col: column of square
        :return: the three rows and three columns that comprise the enclosing square
        """
        if row < 3: rows = [0, 1, 2]
        if 2 < row < 6: rows = [3, 4, 5]
        if 5 < row < 9: rows = [6, 7, 8]
        if col < 3: cols = [0, 1, 2]
        if 2 < col < 6: cols = [3, 4, 5]
        if 5 < col < 9: cols = [6, 7, 8]

        return rows, cols

    def tryValue(self, row, col, val):
        """
        Attempts to place a value in a cell by checking whether the cell has already been
            permanently assigned a value and Sudoku rules
        :param row: row of cell
        :param col: column of cell
        :param val: value to try to assign to cell
        :return: True if value can be placed, false if invalid location,
        """
        rows, cols = self.genSquare(row, col)
        for n in range(0, 9):  # Check column
            if val == self.grid[n, col]:
                return False
            if val == self.grid[row, n]:
                return False
        for r in rows:
            for c in cols:
                if val == self.grid[r, c]:
                    return False
        else:
            return True

    def solve(self, r, c, val):
        """
        Assigns a value to a cell if it is allowed, then returns the next cell
            and value to be attempted
        :param r: row of cell
        :param c: column of cell
        :param val: value to be assigned
        :return: Next cell if assignment is valid or if cell is already filled,
        previous cell and next value to try in previous cell if invalid
        """
        if self.boolgrid[r, c] == 0:
            var = self.tryValue(r, c, val)
            if var == True:
                self.grid[r, c] = val
                return self.forward(r, c)
            elif var == False:
                if val < 9:
                    return r, c, val+1
                else:
                    return self.back(r, c)
        else:
            return self.forward(r, c)

    def forward(self, r, c):
        """
        Returns the next forward cell to solve
        :param r: row
        :param c: column
        :return: Next cell to the right of current, or first cell of next row if
            at end of row
        """
        if c != 8:
            return r, c+1, 1
        else:
            return r+1, 0, 1

    def back(self, r, c):
        """
        Returns the cell to backtrack to when possible values for a cell run out
        Recursive in the case that many multiple backtracks must occur
        :param r: row
        :param c: col
        :return: Next backwards cell, and the next value to try in that cell
        """
        if c != 0:
            lastr = r
            lastc = c - 1
        else:
            lastr = r - 1
            lastc = 8

        lastval = self.grid[lastr, lastc]
        if self.boolgrid[r, c] == 0:
            self.grid[r, c] = 0
        if self.boolgrid[lastr, lastc] == 1:
            return self.back(lastr, lastc)
        elif lastval != 9:
            self.grid[lastr, lastc] = 0
            return lastr, lastc, lastval + 1
        else:
            self.grid[lastr, lastc] = 0
            return self.back(lastr, lastc)

    def solvehelper(grid):
        """
        Handles the solving of the puzzle.  Calls solve function until all cells
            have been filled
        :return: Solved matrix
        """
        r, c = 0, 0
        val = 1
        while r < 9 and c < 9:
            if r < 0 or c < 0:
                return "Cannot be solved"
            result = grid.solve(r, c, val)
            r, c, val = result[0], result[1], result[2]
        return grid.grid

if __name__ == '__main__':
    print "Type each line of puzzle, using spaces or tabs between columns and " \
          "enter at the end of each row.  Substitute zeroes for blank cells:"
    line0 = raw_input('1:   ')
    line1 = raw_input('2:   ')
    line2 = raw_input('3    ')
    line3 = raw_input('4    ')
    line4 = raw_input('5    ')
    line5 = raw_input('6    ')
    line6 = raw_input('7    ')
    line7 = raw_input('8    ')
    line8 = raw_input('9    ')

    a = np.matrix('%s ;%s ;%s ;%s ;%s; %s; %s; %s; %s' % (line0,
                            line1, line2, line3, line4, line5, line6, line7, line8))
    grid = Grid(a)
    print grid.solvehelper()
