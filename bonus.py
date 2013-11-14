from collections import deque
from numpy import array as ar
import numpy

class Bonus(object):
    def __init__(self,gdim,sd = 0.2, nTurn=50,scoreModif=1,col = (160,160,160,200),colNiddle = (30,30,30,200)):
        self.nTurn = nTurn 
        self.gdim = gdim
        self.scoreModif = scoreModif
        self.sd = sd
        self.n = 0
        self.posi = ar([0,0],dtype=int)
        self.colour=col
        self.colNiddle = colNiddle
        
    def tick(self,playerList):
        self.n += 1;
        #~ print self.n 
        if self.n >= self.nTurn:
            self.reSpawn(playerList)
            #~ print '_______'    
            #~ print self.n    
    def reSpawn(self,playerList):
        end = False
        pos = ar([0,0],dtype=int)
        while end == False:
            end = True
            XY= numpy.random.normal(self.gdim/2,self.sd*self.gdim,2).astype(int)
            XY[XY > (self.gdim-1)] = self.gdim-1
            XY[XY < 0] = 0
            for p in playerList:
                for s in p.snake:
                    if sum(s != XY) == 0:
                        end = False
                        break
            self.posi = XY
        
        
        self.n = 0

