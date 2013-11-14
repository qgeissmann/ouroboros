import pyglet

class textDataBase(list):
    def __ini__(self):
        list.__ini__(self)

    def setDataBase(self,game,s,nL):
        self.s = s
        self.nLabels = nL
        
        events = [[st,p,None] for p in game.players for st in p.penalt.listOfPenal]
        rows = [ self.makeNewAnimRow(e,self.s) for e in events]
        for r in rows :
            self.append(r)
     
    def fun(self,event):
        return self.makeNewAnimRow(event,self.s)
        
    def queryAnimList(self,event):
        pena = event[1].penalt.getPenalty(event[0])
        player = event[1]
        l = [w for w in self if w[0] == pena and w[1]== player]
        
        assert len(l) <2
        
        if len(l) == 1:
            return l[0][2]
        else:
            r = self.makeNewAnimRow(event,self.s)
            self.append(r)
            return r[2]
    
            
    def makeNewAnimRow(self,event,s):
        col = event[1].colour_anim
        font = 'Monospace'
        fontMinMax = (self.s//2,self.s*2)
        anims = []
        P = event[1].penalt.getPenalty(event[0])
        text = '%i' % - P
        if P < 0:
            text = '+'+text
        for i in range(self.nLabels):
            fs = self.calcFontSize(fontMinMax,i)
            label =  pyglet.text.Label(text,\
                                    font_name=font,\
                                    font_size=fs,\
                                    x=0,\
                                    y=0,\
                                    color = col,\
                                    anchor_x='left',\
                                    anchor_y='bottom')
            anims.append(label)
            
        pena = event[1].penalt.getPenalty(event[0])
        player = event[1]
        row = [pena,player,anims]
        return row
        
    def calcFontSize(self,fontMinMax,i):
        tf = i*1.0 /self.nLabels   
        mi = fontMinMax[0]
        ma = fontMinMax[1]
        return (ma - mi)*(tf**(1/1.5)) +mi    
        
            
class AnimationHandler:
    def __init__(self,game,offset,s):
        self.gameEvent = game.gameEvent
        self.players = game.players
        self.gdim = game.dim
        self.offset = offset
        self.s = s
        self.liveAnims = list()
        self.tdb = textDataBase()
        self.tdb.setDataBase(game,self.s,24)
        
    def playQueuedAnim(self):
        while len(self.gameEvent)>0:
            e = self.gameEvent.pop()
            self.runAnimation(e)
            
    def runAnimation(self,e): 
            listOfLabs = self.tdb.queryAnimList(e)
            xy = e[2] * self.s + self.offset
            self.liveAnims.append(TextAnim(listOfLabs,xy,self.s))
            
    def renderAllAnims(self):
        self.playQueuedAnim()
        for l in self.liveAnims:
            if l.isAlive:
                l.label.draw()
            else:
                self.liveAnims.remove(l)
    
class TextAnim(object):    
    def __init__(self,listOfAnim,xy,s,time = 0.5):        
        self.la = listOfAnim
        self.xy = xy
        self.s = s
        self.T = time
        self.t = 0
        self.label = pyglet.text.Label()
        self.isAlive = True
        pyglet.clock.schedule_interval(self.play,1.0/24)
        
    def play(self,t):
        self.t+=t
        if self.t > self.T:
            self.t = self.T
        idxInLa = int(((len(self.la))*self.t)/self.T)-1
        addiOffset = int((self.s*2.2*self.t/self.T)**(1/2))
        self.label = self.la[idxInLa]
        self.label.x = self.xy[0] +addiOffset
        self.label.y = self.xy[1] +addiOffset
        if self.t >= self.T:
            pyglet.clock.unschedule(self.play)
            self.isAlive = False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        #~ self.xy = self.startPos * self.s + self.offset            
#~ class TextAnim(object):    
    #~ def __init__(self,event,offset,s,time = 0.5):        
        #~ self.col = event[1].colour_anim
        #~ P = event[1].penalt.getPenalty(event[0])
        #~ self.text = '%i' % - P
        #~ if P < 0:
            #~ self.text = '+'+self.text
        #~ 
        #~ self.startPos = event[2]
        #~ self.offset = offset
        #~ self.s = s
        #~ self.font = 'Monospace'
        #~ self.fontMinMax = (self.s//2,self.s*2)
        #~ self.T = time
        #~ self.t = 0
        #~ self.isAlive = True
        #~ self.xy = self.startPos * self.s + self.offset
        #~ 
        #~ 
        #~ 
        #~ self.label =  pyglet.text.Label(  self.text,\
                                    #~ font_name=self.font,\
                                    #~ font_size=s,\
                                    #~ x=self.xy[0],\
                                    #~ y=self.xy[1],\
                                    #~ color = self.col,\
                                    #~ anchor_x='left',\
                                    #~ anchor_y='bottom')
                                    #~ 
        #~ self.updateFontSize()
        #~ pyglet.clock.schedule_interval(self.play,1.0/60)
#~ 
    #~ def updateFontSize(self):
        #~ tf = self.t*1.0 /self.T        
        #~ mi = self.fontMinMax[0]
        #~ ma = self.fontMinMax[1]
        #~ self.label.font_size = (ma - mi)*(tf**(1/1.5)) +mi
         #~ 
        #~ 
    #~ def play(self,dt):
        #~ self.t += dt
#~ 
        #~ self.updateFontSize()
#~ 
        #~ if self.t > self.T:
            #~ pyglet.clock.unschedule(self.play)
            #~ self.isAlive = False
        
