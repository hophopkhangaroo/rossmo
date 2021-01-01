class Point():
    '''Creates coordinate points with values (x,y)'''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def taxicab_distance(self, other):
        '''Returns distance using taxicab metric'''
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        return dx + dy
