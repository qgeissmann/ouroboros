from snake import *

class Penalties:
    #~ def __init__(self,touch_foe = 99999,touch_self =50,take_bonus = -2,foe_bonus = 1,boost = 3):
    def __init__(self,touch_foe = 4,touch_self =3,take_bonus = -1,foe_bonus = 1,boost = 2):
    #~ def __init__(self,touch_foe = 99999,touch_self =50,take_bonus = -0,foe_bonus = 4,boost = 3):
         self.touch_foe = touch_foe
         self.touch_self = touch_self
         self.take_bonus = take_bonus
         self.foe_bonus = foe_bonus
         self.boost = boost
         self.listOfPenal = ['touch_foe','touch_self','take_bonus','foe_bonus','boost']
    def getPenalty(self,strg):
        if(strg == 'touch_foe'):
            return self.touch_foe
        elif(strg == 'touch_self'):
            return self.touch_self
        elif(strg == 'take_bonus'):
            return self.take_bonus
        
        elif(strg == 'foe_bonus'):
            return self.foe_bonus
            
        elif(strg == 'boost'):
            return self.boost
        else:
            return 9999999
    
class Player(object):
    class_counter= 0 
    #~ def __init__(self,game,LURD,palette,penalt = Penalties(),iniL = 200):
    def __init__(self,game,LURD,palette,penalt = Penalties(),iniL = 100):
    #~ def __init__(self,game,LURD,palette,penalt = Penalties(),iniL = 20):
        
        self.colour_anim = palette.colAnims
        self.colour = palette.colSegment
        
        self.penalt = penalt
        self.iniLength = iniL
        self.LURD = LURD
        self.dirStr = ['left','up','right','down']
        self.keyStack = list()
        self.snake=Snake()
        
        self.game = game
        Player.class_counter+=1
        
    def keyFilter(self,symb):
        for i,l in enumerate(self.LURD):
            if symb == l:
                self.keyStack.append(self.dirStr[i])
                
    def moveMySnakeOne(self,count):
        if self.snake.isAlive:
            self.snake.moveOne(self.keyStack,count)
        
    def cleanMySnake(self): 
        if self.snake.isAlive:
            self.snake.clean()    
    def preChopMySnake(self,strg):  
        #~ assert len(self.snake)>0
        if self.snake.isAlive:
            nToChop = self.penalt.getPenalty(strg)
            self.snake.preChop(nToChop)
            
    def boostMySnake(self):      
        if self.snake.isAlive:
            self.snake.hasBoost=True
    def killMySnake(self):    
        if self.snake.isAlive:
            self.snake.isAlive = False
            self.snake.clean()
        
