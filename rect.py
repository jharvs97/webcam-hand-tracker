import numpy as np

class Rect:

    def __init__(self, minX, minY, w, h):
        self.minX = int(minX)
        self.minY = int(minY)
        self.maxX = int(minX + w)
        self.maxY = int(minY + h)
        self.maxXY = (self.maxX, self.maxY)
        self.minXY = (self.minX, self.minY)
    
    
