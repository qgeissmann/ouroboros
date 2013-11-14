from collections import deque
from numpy import array as ar
import numpy

class Snake(deque):
    def __init__(self,length = 0,posi = ar([0,0]) , direc = ar([0,1])):
        deque.__init__(self)
        self.ini_snake(length,posi,direc)
        
             
       
        
    def reset(self,length,posi,direc):
        self.clear()
        self.ini_snake(length,posi,direc)
        
    def ini_snake(self,length,posi,direc):
        for i in range(length):
            self.append(posi)
        self.direc = direc
        self.count = 0
        self.history = list()
        self.dirStack = deque()
        self.isAlive = True
        self.hasBoost = False
        self.nToChop = 0
    def clean(self):
        self.chop()
        if len(self) < 2:
            self.isAlive=False
        self.hasBoost = False
        
        if not self.isAlive:
            self.clear()
        
    def preChop(self,c):
        self.nToChop += c
        
        
    def chop(self):
        if self.isAlive:
            if self.nToChop > 0:
                for i in range(0,1+self.nToChop//2):
                    if(len(self)>0):
                        self.pop()
                        self.nToChop -=1
            elif self.nToChop < 0:
                posiLast = self[len(self)-1]
                for i in range(0,-self.nToChop):
                    if(len(self)>0):
                        self.append(posiLast)
                        self.nToChop += 1
                        
    def moveOne(self,keyStack,count):
        if(self.isAlive):
            self.count = count
            self.changeDir(keyStack)
            head = self[0] + self.direc
            self.appendleft(head)
            self.pop()
    

    def changeDir(self,keyStack):
        if len(self.dirStack) == 0:
            if len(keyStack) >0:
                if len(keyStack) == 1 or len(keyStack) > 2:
                    k = keyStack[0]
                    newDir = self.stringToDir(k)
                    
                elif len(keyStack) == 2:
                    newDir = self.twoKeysToStack(keyStack)
                
                self.checkAndSetDir(newDir)
            
        else:
            self.checkAndSetDir(self.dirStack[0])
            self.dirStack.popleft()

    def twoKeysToStack(self,keyStack):
        self.dirStack = deque()
        s = [self.stringToDir(k) for k in keyStack]
        sameKeys = (sum(s[0] == s[1]) == 2)
        opositeKeys = (sum((s[0] + s[1]) == 0) != 0)
        if sameKeys or opositeKeys :
            return s[0]
        else:
            if numpy.vdot(self.direc,s[0]) == 0:
                self.dirStack.append(s[1])
                return s[0]
            else:
                self.dirStack.append(s[0])
                return s[1]

    def pushEventinHistory(self,event):
        self.history.append((event,self.count))
        
    def checkAndSetDir(self,newDir):
        if sum(newDir == self.direc) == 2:
            self.hasBoost = True
            self.pushEventinHistory('boost')
        elif sum((newDir + self.direc) == 0) == 0:
            self.direc = newDir
            self.pushEventinHistory(('dirTo',newDir))

    def stringToDir(self,strg):
        if strg == 'left':
            return ar([-1,0])
        elif strg == 'up':
            return ar([0,1])
        elif strg == 'right':
            return ar([1,0])
        elif strg == 'down':
            return ar([0,-1])
