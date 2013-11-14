import pyglet
from game import *
from openGLSetter import *
from animations import *
from snakeDrawer import *
from bonusDrawer import *
from backgroundDrawer import *


   

    
class MyWindow(pyglet.window.Window):
    
    def __init__(self,game ,context,showFps = True,FS=True):
        pyglet.window.Window.__init__(self,context=context,fullscreen=FS)
        
        self.minOffsetProp = 20
        self.showFps = showFps
        self.game = game
        self.fpsDisplay = pyglet.clock.ClockDisplay()

        scale, offset = self.ini_calcAB()
        
        self.batch = pyglet.graphics.Batch()
        
        self.AnimHand =  AnimationHandler(game,offset ,scale)
        self.snakeDrawer = [SnakeDrawer(p.snake,offset,scale,p.colour) for p in self.game.players ]
        self.bgd = BackgroundDrawer(offset,scale,game.dim)
        self.bonDra = BonusDrawer(self.game.bonusList,offset,scale)
        
        #~ 
        gl.glEnable( gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST);
        #~ 
        #~ gl.glDisable(gl.GL_POLYGON_SMOOTH)
        
        #~ gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST);

    def on_draw(self): 
        self.clear()
        
        
        gl.glEnable(pyglet.gl.GL_LINE_SMOOTH);
        self.bgd.render()
        self.bonDra.render()  
        
        
        
        for sd in self.snakeDrawer: #
            sd.render()
        
        gl.glDisable(pyglet.gl.GL_LINE_SMOOTH);
            
        self.AnimHand.renderAllAnims()
        #~ 
        if self.showFps:
            self.fpsDisplay.draw()
       
    def on_key_press(self,symbol,modifiers):
        if symbol == pyglet.window.key.DELETE or  symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.SPACE:
            if self.game.pause == True:
                self.game.pause = False
            else:
                self.game.pause = True
        else:
            for s in self.game.players:
                s.keyFilter(symbol)         
            return False
            
    def ini_calcAB(self):
        w = self.width
        h = self.height
        dim = self.game.dim
        m = h//self.minOffsetProp
        
        assert w > h    
        o = ((h - 2 * m ) % (dim-1)) // 2
        vo = o+m
        ho = o+m+(w-h)/2 
        s = (h - 2 * (vo)) // (dim-1)
        
        return (s,(ho,vo))
