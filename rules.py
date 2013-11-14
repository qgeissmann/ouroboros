
from player import *
from numpy import array as ar
import numpy as np

class Rules:
    def __init__(self,players,bonusList,gameWidth):
        self.players = players
        self.gameWidth = gameWidth
        self.bonusList = bonusList
        self.gameEvent = list()
    def apply(self,player,count):
        s = player.snake
        self.gameEvent = list()
        
        ts = self.touchSelf(s)
        if(ts):
            player.preChopMySnake('touch_self')
            self.gameEvent.append(('touch_self',player,s[0]))
            
        tf = self.touchFoe(s)
        if(tf):
            player.preChopMySnake('touch_foe')
            self.gameEvent.append(('touch_foe',player,s[0]))
            
        tb = self.touchBonus(s)
        if(tb):
            player.preChopMySnake('take_bonus')
            self.gameEvent.append(('take_bonus',player,s[0]))
            
        bo = self.boost(s)
        if(bo):
            player.boostMySnake()
            player.preChopMySnake('boost')
            self.gameEvent.append(('boost',player,s[0]))
                
        tl = self.touchWall(s)
                
        if(tl):
            p = np.copy(s[0])
            player.killMySnake()
            self.gameEvent.append(('die',player,p))
        #~ 
        #~ print self.gameEvent
        return self.gameEvent
    
    
    
    def touchWall(self,s):
        if s.isAlive:
            head = s[0]
            if np.any(head < 0) or np.any(head > self.gameWidth-1):
                    return True
        return False
        
    def touchBonus(self,s):
        if s.isAlive:
            head = s[0]
            for b in self.bonusList:
                if sum(b.posi != head) == 0:
                    b.n=b.nTurn+1 ## force respawn at next turn
                    for pp in [p for p in self.players if p.snake is not s and p.snake.isAlive]:
                        pp.preChopMySnake('foe_bonus')
                        self.gameEvent.append(('foe_bonus',pp,pp.snake[0]))
                    return True
        
        return False
    def touchSelf(self,s):
        if s.isAlive:
            head = s[0]
            for i,p in enumerate(s):
                if sum(p != head) == 0 and i > 0:
                    return True
        return False
            
    def touchFoe(self,s):
        if s.isAlive:
            head = s[0]
            for pp in self.players:
                foe = pp.snake 
                if s is not foe and foe.isAlive:
                    for pf in foe:
                        if sum(pf != head) == 0:
                            return True
        return False
        
    def boost(self,s):
        if s.isAlive:
            if s.hasBoost:
                return True
        return False
