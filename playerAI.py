from player import *
from numpy import array as ar
import numpy as np
import C_AI
from multiprocessing import Pool


def fun(arg):
    if len(arg) > 1:
        scoreMat = arg[0]
        s0 = arg[1]
        bonus = np.zeros((1,1),dtype = int) #no used !
        out = np.zeros(scoreMat.shape,dtype=int)
        C_AI.Lee2(scoreMat,s0,bonus,out)
        return out
    else:
        return ar([0])
            
class PlayerAI(Player):
    def __init__(self,game,palette,penalt = Penalties()):
        LURD=None
        Player.__init__(self,game,LURD,palette,penalt = Penalties())
        self.SELF_SCORE = 10
        self.FOE_SCORE = 20
        self.pool = Pool(4)
        
    def moveMySnakeOne(self,count):
        if self.snake.isAlive:
            self.findDirection()
            if self.snake.isAlive:
                self.snake.moveOne(self.keyStack,count)
            
    
    
    def findDirection(self):
        sm = self.makeScoreMap()
        dbm,cm = self.makeClimbMat(sm)
        bestBonIdx = self.findBestBonus(dbm)
        dire = self.snake.direc
        if bestBonIdx > -1:
            goTo = self.game.bonusList[bestBonIdx].posi
            dire = self.findPath(cm,goTo) 
        #~ Else, we pick randomly a point near the middle:
        else:
            found = False
            i = 0.05
            while (found == False and i < 0.5):                
                XY = np.random.normal((self.game.dim-1)/2,i*self.game.dim,2).astype(int)
                #~ Determines validity of the point:
                #~ The 3x3 area around is empty
                area = cm[XY[0]-1:XY[0]+2,XY[1]-1:XY[1]+2]
                
                t0 = (np.sum(area < 0) == 0)
                t1 = np.all(XY > 0)and np.all(XY < self.game.dim)
                
                test = t0 and t1
                if test:
                    dire = self.findPath(cm,XY)
                    found=True
                else:
                    i+=0.05
            #~ by default:
            
            if found == False:
                dire = ar([0,0])
                toCent = self.snake[0] - self.game.dim/2
                q = max(abs(toCent))
                if not q==0:
                    toCent = -toCent/q
                    if toCent[0] == toCent[1]:
                            if toCent[0] == 1:
                                toCent[0] = 0
                            if toCent[0] == -1:
                                toCent[0] = 0
                            if toCent[0] == 0:
                                toCent[0] = 1
                    dire = toCent
                else:
                    dire = ar([1,0])
        
        self.addDirAsKeyStack(dire)
        
    def makeScoreMap(self):
        scoreMap = np.zeros((self.game.dim,self.game.dim),dtype=int)
        for p in self.game.players:
            s = p.snake
            if s.isAlive:
                if s is self:
                    toAdd = self.SELF_SCORE 
                else:
                    toAdd = self.FOE_SCORE 
                for m in s:
                    scoreMap[m[0],m[1]] += toAdd
        return scoreMap
        
        
    def makeClimbMat(self,scoreM):
        Nb = self.game.nBonus
        Ns = len(self.game.players)
        
        distBonusMat = np.ones((Nb,Ns),dtype = int)
        bonus = np.zeros((Nb,2),dtype = int)
        myClimbMat = np.zeros(scoreM.shape,dtype=int)
        for i in range(Nb):
            b = self.game.bonusList[i]
            bonus[i] = b.posi
            


        args = [ [scoreM,p.snake[0]] if p.snake.isAlive else []  for p in self.game.players ]
        
        C_out = self.pool.map(fun,args)

        for i in range(Ns):
            s = self.game.players[i].snake
            if s.isAlive:
                if self is self.game.players[i]:
                    myClimbMat = np.copy(C_out[i])
                distBonusMat[:,i] = self.makeOneCol(C_out[i],bonus)
            else:
                distBonusMat[:,i] = -1

        for i in range(Nb):
            b = self.game.bonusList[i]
            t = b.nTurn  - b.n
            pos = b.posi
            if myClimbMat[pos[0],pos[1]] > t:
                distBonusMat[i] = -1
               
        return distBonusMat,myClimbMat
        
    #~ 
    def makeClimbMat(self,scoreM):
        Nb = self.game.nBonus
        Ns = len(self.game.players)
        
        distBonusMat = np.ones((Nb,Ns),dtype = int)

        bonus = np.zeros((Nb,2),dtype = int)
        
        myClimbMat = np.zeros(scoreM.shape,dtype=int)
        C_out = np.zeros(scoreM.shape,dtype=int)

        for i in range(Nb):
            b = self.game.bonusList[i]
            bonus[i] = b.posi
        
        for i in range(Ns):
            s = self.game.players[i].snake
            if s.isAlive:
                C_AI.Lee2(scoreM,s[0],bonus,C_out) #TODO does not need/use bonus!
                if self is self.game.players[i]:
                    myClimbMat = np.copy(C_out)
                distBonusMat[:,i] = self.makeOneCol(C_out,bonus)
            else:
                distBonusMat[:,i] = -1
        
        for i in range(Nb):
            b = self.game.bonusList[i]
            t = b.nTurn  - b.n
            pos = b.posi
            if myClimbMat[pos[0],pos[1]] > t:
                distBonusMat[i] = -1
               
        return distBonusMat,myClimbMat
        
    
    
    #~ 
    #~ 
    
    
    
    
    
    
    
    
    
    
    
    
    
    def makeOneCol(self,scoreMap,bonus):
        Nb = self.game.nBonus
        col = np.ones((Nb),dtype = int)
        for i in range(len(bonus)):
            col[i] = scoreMap[bonus[i][0],bonus[i][1]]
        return col  
    def findBestBonus(self,mat):
        # a snipet to fin
        wichSnake = -1
        Ns = len(self.game.players)
        for i,p in enumerate(self.game.players):
            if p is self:
               wichSnake = i
               break
        assert wichSnake >=0

        vec = np.copy(mat[:,wichSnake],)
        
        mat[:,wichSnake] = -1
        
        rank  = vec.argsort()
        foundBest = -1
        for i in rank:
            if vec[i] > -1:
                if foundBest == -1:
                    best = vec[i]
                    row = mat[i]
                    row = row[row>0]
                    nBetter  = sum(row <= best)
                    if nBetter == 0:
                        foundBest = i
        return foundBest             
    def findPath(self,a,start):
        
        tmp = start
        last = np.copy(tmp)
        end = False
        lim = self.game.dim-1
        while(end == False):
            if tmp[0] < lim   and a[tmp[0]+1,tmp[1]] < a[tmp[0],tmp[1]]and a[tmp[0]+1,tmp[1]] >= 0:
                last = numpy.copy(tmp)
                tmp = ar([tmp[0]+1,tmp[1]])
                
            elif tmp[0]>0 and a[tmp[0]-1,tmp[1]]< a[tmp[0],tmp[1]]and a[tmp[0]-1,tmp[1]] >= 0:
                last = np.copy(tmp)
                tmp = ar([tmp[0]-1,tmp[1]])            
                
            elif tmp[1] < lim and a[tmp[0],tmp[1]+1]< a[tmp[0],tmp[1]]and a[tmp[0],tmp[1]+1] >= 0:
                last = np.copy(tmp)
                tmp = ar([tmp[0],tmp[1]+1])
                
            elif tmp[1]>0 and a[tmp[0],tmp[1]-1]< a[tmp[0],tmp[1]] and a[tmp[0],tmp[1]-1] >= 0:
                last = np.copy(tmp)
                tmp = ar([tmp[0],tmp[1]-1])
            
            else:
                end=True
                
        dire = last - self.snake[0]
        return dire
    def addDirAsKeyStack(self,dire):
        dirStr=''
        
        if sum(dire == ar([-1,0],dtype=int)) == 2:
            dirStr="left"            
        elif sum(dire == ar([1,0],dtype=int)) == 2:
            dirStr="right"
        elif sum(dire == ar([0,-1],dtype=int)) == 2:
            dirStr= "down"
        elif sum(dire == ar([0,1],dtype=int)) == 2:
            dirStr="up" 
        if sum(dire == self.snake.direc) == 2: #avoid boost
            dirStr =''
            

        if dirStr != '':
           
            self.keyStack.append(dirStr)
    def keyFilter(self,symb):
        pass 






        #~ for i in range(Ns):
            #~ s0 = self.game.players[i].snake[0]
            #~ if s.isAlive:
                #~ threading.Thread(target=test, args=(s0,scoreM.shape,scoreM))
                #~ 
                #~ threads.append(t)
                #~ t.start()
            

            
         #TODO does not need/use bonus!
        #patch to negate un reacheable bonuses:
