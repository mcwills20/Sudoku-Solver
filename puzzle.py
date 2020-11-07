class box(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Get what quadrant the block is in. Useful for checking later
        self.quad = self.getquad()
        # Initialize the possible dict
        self.initpossible()

    # When printing, display the value    
    def __repr__(self):
        return str(self.value)


    def getquad(self):

        if self.row <= 2:
            # Upper left
            if self.column <= 2:
                return 1
            # Upper Right
            elif self.column >= 6:
                return 3
            # Upper Middle
            else:
                return 2
        elif self.row >= 6:
            # Middle Left
            if self.column <= 2:
                return 4
            # Middle Right
            elif self.column >= 6:
                return 6
            # True Middle
            else:
                return 5
        else:
            # Lower Left
            if self.column <= 2:
                return 7
            # Lower Right
            elif self.column >= 6:
                return 9
            # Lower Middle
            else:
                return 8


    def initpossible(self):
        self.possible = dict()
        if self.value == 0:
            for i in range(1,10):
                self.possible[i] = True
        else:
            for i in range(1,10):
                self.possible[i] = False

            self.possible[self.value] = True

