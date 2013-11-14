import pyglet

class BackgroundDrawer:
    def __init__(self,offset,s,gdim):
        x0 = offset[0]
        y0 = offset[1]
        colGrid = (64,64,64,128) 
        colBord = (128,128,128,128) 
        colBack = (43,32,18,125) 
          
        self.batch = pyglet.graphics.Batch()
        self.ini_addBorderToBash(gdim,s,x0,y0,colBord)
        self.ini_addGridToBash(gdim,s,x0,y0,colGrid)
        self.ini_addSquareToBash(gdim,s,x0,y0,colBack)
        self.lw = s*0.10 

        
    
    def ini_addSquareToBash(self,gdim,s,x0,y0,col):
        k = s*(gdim-1) 

        p0 =  (x0,y0)
        p1=  (x0+k,y0)
        p2 =  (x0+k,y0+k)
        p3 =  (x0,y0+k)
        vertexPos = p0 + p1  + p2 + p2  +p3 
        
        self.batch.add(5,pyglet.gl.GL_TRIANGLE_FAN,None,('v2i',vertexPos),('c4B',col*5))
        
    def ini_addBorderToBash(self,gdim,s,x0,y0,col):
        k = s*(gdim-1) 

        p0 =  (x0,y0)
        p1=  (x0+k,y0)
        p2 =  (x0+k,y0+k)
        p3 =  (x0,y0+k)
        vertexPos = p0 + p1  + p2  +p3 
        self.batch.add(4,pyglet.gl.GL_LINE_LOOP,None,('v2i',vertexPos),('c4B',col*4))
        
    def ini_addGridToBash(self,gdim,s,x0,y0,col):
        k = s*(gdim-1)
        vpos = tuple()
        hpos = tuple()
        for i in range(1,gdim-1):
            x =x0 + s*i 
            vpos += ((x,y0)+(x,y0+k))
            y =y0 + s*i 
            hpos += ((x0,y)+(x0+k,y))

        n = (gdim-2) *2
        self.batch.add(n,pyglet.gl.GL_LINES,None,('v2i',vpos),('c4B',col*n))
        self.batch.add(n,pyglet.gl.GL_LINES,None,('v2i',hpos),('c4B',col*n))
        
    def render(self):
        pyglet.gl.glLineWidth(self.lw)
        self.batch.draw()
        
