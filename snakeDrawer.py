import pyglet
import numpy as np
from numpy import array as ar

from openGLSetter import *

class SegmentDrawer:
    
    def __init__(self,snake,batch,i,of,s,col,fillSeg = True,nVert=5):
        self.batch = batch
        self.minMaxAlpha = (128,255)
        self.lw = s*0.1
        self.fillSeg = fillSeg
        self.col0 = col
        self.col1 = col
        self.s = s
        self.offset = of
        self.idx = i
        
        self.snake = snake
        self.oldSnakeLength = len(self.snake)
        self.posi = self.snake[self.idx]
        self.oldPosi = np.copy(self.posi)
        self.nVertexPerCircle = nVert+1
        self.ini_makeVertices()
        self.updateAlpha()
        
    def __del__(self):
        if self.fillSeg:
            self.fill.delete()
        self.contours.delete()
        
    def ini_makeVertices(self):
        self.preCalcVal = self.ini_preCalCosSin(rot = (len(self.snake) - self.idx)**.5)
        l = self.calcCircleVert()
        c0 = self.col0 * (len(l)/2)
        c1 = self.col1 * (len(l)/2)
        idxLines = [i for i in range(len(l)/2) for _ in range(2)][1:len(l)-1]     
        self.contours = self.batch.add_indexed(len(l)/2,pyglet.gl.GL_LINES,None,idxLines,('v2f',l),('c4B',c0)) 
        if self.fillSeg :
            idxTriangles = [j for i in range(1,len(l)/2-1) for j in [0,i,i+1] ]
            self.fill = self.batch.add_indexed(len(l)/2,pyglet.gl.GL_TRIANGLES,None,idxTriangles,('v2f',l),('c4B',c1))
            
    def updateAlpha(self):
        pl = self.idx * 1.0 / len(self.snake)
        return int(self.minMaxAlpha[1] - (self.minMaxAlpha[1]-self.minMaxAlpha[0]) *  pl)
        
    def calcCircleVert(self):
        xy =self.posi * self.s
        l = list((self.preCalcVal + xy).reshape(self.nVertexPerCircle*2))
        return l
        
    def ini_preCalCosSin(self,rot = 0):
        a = np.linspace( 0, np.pi*2,self.nVertexPerCircle )
        co = np.cos(a + rot)*self.s/2+self.offset[0]
        si = np.sin(a + rot)*self.s/2+self.offset[1]
        return np.vstack([co,si]).transpose()        
    def update(self):
        self.posi = self.snake[self.idx]
        if np.any(self.oldPosi != self.posi):
            v = self.calcCircleVert()
            self.contours.vertices = v
            if self.fillSeg:
                self.fill.vertices = v
                
            if self.oldSnakeLength != len(self.snake):
                col = (self.col0[0:3] + (self.updateAlpha(),))*(self.nVertexPerCircle)
                if self.fillSeg:
                    self.fill.colors[:] = col
                    
        self.oldPosi = np.copy(self.posi)
        self.oldSnakeLength = len(self.snake)
    
class HeadSegmentDrawer(SegmentDrawer):
    
    def __init__(self,snake,batch,i,of,s,col):
        SegmentDrawer.__init__(self,snake,batch,i,of,s,col,True,nVert = 32)
        self.minMaxAlpha = (132,132)
        self.lw = s*0.2
        l = self.calcAntenaVert()
        c0 = self.col0 * (len(l)/2)
        self.anten = self.batch.add(len(l)/2,pyglet.gl.GL_LINE_STRIP,None,('v2f',l),('c4B',c0))
        
    def __del__(self):
        self.anten.delete()
        SegmentDrawer.__del__(self)
        
    def calcAntenaVert(self):
        xy =self.posi * self.s + self.offset
        d = self.snake.direc
        rotMat = np.vstack([d,d[::-1]]) 
        
        v = ar([self.s,0.5*self.s])
        w = ar([self.s,-0.5*self.s])
        vv = xy + np.dot(rotMat,v)
        ww = xy + np.dot(rotMat,w)
        
        r = np.vstack([vv,xy,ww]).reshape(6)
        return list(r)

    def update(self):
        self.posi = self.snake[self.idx]
        self.anten.vertices = self.calcAntenaVert()
        if np.any(self.oldPosi != self.posi):
            v = self.calcCircleVert()
            self.contours.vertices = v
        SegmentDrawer.update(self)
        
class SnakeDrawer:
    def __init__(self,snake,of,s,col):
        self.snake = snake
        self.of = of
        self.s = s
        self.col = col
        self.oldLength = len(snake)
        self.segments = list()
        self.batch = pyglet.graphics.Batch() 
        
        for i in range(len(snake)):
            if i < 1 :
                self.segments.append(HeadSegmentDrawer(snake,self.batch,i,self.of,self.s,self.col) )
            else:
                self.segments.append(SegmentDrawer(snake,self.batch,i,self.of,self.s,self.col))

    def render(self):
        diff = self.oldLength - len(self.snake)
        if diff > 0:
            len(self.snake)
            for i in range(diff): 
                self.segments.pop() 
        elif diff < 0:
            for i in range(self.oldLength,len(self.snake)):
                if i < 1 :
                    self.segments.append(HeadSegmentDrawer(self.snake,self.batch,i,self.of,self.s,self.col) )
                else:
                    #~ pass
                    self.segments.append(SegmentDrawer(self.snake,self.batch,i,self.of,self.s,self.col) )
        
        for d in self.segments:
            d.update()
        self.oldLength  =  len(self.snake)
        self.batch.draw()









