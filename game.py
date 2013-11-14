
from rules import *
from bonus import *
from numpy import array as ar
import numpy

class Game(object):
    

    def __init__(self,dim=50,nBonus=1 ):
        #~ self.pause = True
        self.pause = False
        self.count=0
        self.totalTime = 0.0
        self.dim = dim
        self.players = list()
        self.bonusList = list() 
        self.gameEvent = list()
        
        self.nBonus = nBonus
        self.rules = Rules(self.players,self.bonusList,self.dim)
       
        
    def addNewPlayer(self,player):
        self.players.append(player)
        self.ini_snakes(self.players)
        self.ini_bonus()
        
    def reset(self):  
        pdl = self.ini_makePosiDirList()
        for i,p in enumerate(self.players):
            l = p.iniLength
            p.snake.reset(p.iniLength,posi = pdl[i][0],direc = pdl[i][1])
            self.ini_bonus()
        self.totalTime = 0
        self.count = 0
        #~ self.pause = True
            
    def ini_bonus(self):  
        del self.bonusList[:]
        for i in range(self.nBonus):
            b = Bonus(self.dim)
            b.reSpawn(self.players)
            self.bonusList.append(b)
                
    def ini_makePosiDirList(self):
        thr = self.dim/(len(self.players) * 5)
        center = ar([self.dim//2,self.dim//2],dtype = int)
        pdl = list()
        while len(pdl) < len(self.players):
            r = numpy.random.rand(2)
            XY = (numpy.around((center-self.dim//10)*2*r)+self.dim//10).astype(int)
            ok = True
            for j in pdl:#check distance
                if sum(abs(XY - j[0])) < thr:
                    ok = False
            if ok: 
                r = numpy.random.randint(4)
                if r == 0:
                    pdl.append((XY,ar([-1,0])))
                elif r ==1:
                    pdl.append((XY,ar([0,1])))
                elif r ==2:
                    pdl.append((XY,ar([1,0])))
                elif r ==3:
                    pdl.append((XY,ar([0,-1])))
        return pdl
        
    def ini_snakes(self,players):
        snakes = list()
        pdl = self.ini_makePosiDirList()
        for i,p in enumerate(self.players):
            l = p.iniLength
            sn = Snake(p.iniLength,posi = pdl[i][0],direc = pdl[i][1])
            p.snake = sn


        
    def playOnce(self,dt=0):  
        if not self.pause:
            nAlive =  len([True for p in self.players if p.snake.isAlive  ])
            if  len(self.players) > 1:
                if nAlive < 2:
                    self.reset()
            elif nAlive < 1: 
                self.reset()
                        
                
            for p in self.players:
                p.moveMySnakeOne(self.count)
                p.keyStack = list()
                self.gameEvent += self.rules.apply(p,self.count)
                
                    
            for p in self.players:
                if p.snake.hasBoost:
                    p.snake.hasBoost = False
                    p.moveMySnakeOne(self.count)
                    self.gameEvent += self.rules.apply(p,self.count)
                
            for b in self.bonusList:
                b.tick(self.players)
                
            for p in self.players:
                p.cleanMySnake()
            
            self.totalTime +=dt
            self.count += 1
            if self.count %500 == 0:
                print(self.totalTime,self.count)
                #~ exit()

    def playLoop(self,dum):
        while True:
            self.playOnce()
        
        
