import pyglet
import numpy as np
from openGLSetter import *

class BonusDrawer:
    def __init__(self,bonusList,offset,s):
        self.lw = s*0.1 
        self.s = s
        self.offset = offset
        self.bonusList = bonusList
        
        self.nVertexPerCircle = 17
        
        self.batch = pyglet.graphics.Batch()
        
        self.oldPosi = list()
        for b in self.bonusList:
            self.oldPosi.append(np.array([-1,-1]))

        self.listOfLists = list()
        self.preCalcVal = self.ini_preCalCosSin()

        for i,b in enumerate(self.bonusList):
            l = self.calcCircleVert(b)
            v = self.calcNiddlePos(b)
            #~ c0 =
            c0 = b.colour * (len(l)/2)
            c1 = b.colNiddle * (len(l)/2)
            c2 = b.colNiddle * 2

            idxLines = [i for i in range(len(l)/2) for _ in range(2)][1:len(l)-1]  
            idxTriangles = [j for i in range(1,len(l)/2-1) for j in [0,i,i+1] ]   

            self.listOfLists.append([
                                        #~ self.batch.add(len(l)/2,pyglet.gl.GL_LINE_LOOP,None,('v2f',l),('c4B',c0)),\
                                        self.batch.add_indexed(len(l)/2,pyglet.gl.GL_LINES,None,idxLines,('v2f',l),('c4B',c1)),\
                                        #~ self.batch.add(len(l)/2,pyglet.gl.GL_POLYGON,None,('v2f',l),('c4B',c1)),\
                                        self.batch.add_indexed(len(l)/2,pyglet.gl.GL_TRIANGLES,None,idxTriangles,('v2f',l),('c4B',c0)),\
                                        #~ self.batch.add(len(l)/2,pyglet.gl.GL_POLYGON,None,('v2f',l),('c4B',c1)),\
                                        self.batch.add(2,pyglet.gl.GL_LINES,None,('v2f',v),('c4B',c2)),\
                                    ])
        
    def ini_preCalCosSin(self):
        a = np.linspace( 0, np.pi*2,self.nVertexPerCircle )
        co = np.cos(a)*self.s/2+self.offset[0]
        si = np.sin(a)*self.s/2+self.offset[1]
        return np.vstack([co,si]).transpose()
        
    def updateVertices(self,idx):
        bonus = self.bonusList[idx]
        self.listOfLists [idx][2].vertices = self.calcNiddlePos(bonus)
        if sum(self.oldPosi[idx] == bonus.posi) < 2 :
            self.listOfLists [idx][0].vertices = self.calcCircleVert(bonus)
            self.listOfLists [idx][1].vertices = self.calcCircleVert(bonus)

    def calcNiddlePos(self,bonus):
        t = bonus.n
        T = bonus.nTurn
        a = (1-t*1.0/T) * np.pi*2 + np.pi/2

        xy = self.offset + bonus.posi*self.s
        x1y1 = xy + np.array([np.cos(a),np.sin(a)])*self.s/1.7

        v = list(np.hstack([xy,x1y1]))

        return v
        
    def calcCircleVert(self,bonus):
            xy = bonus.posi*self.s
            l = list((self.preCalcVal + xy).reshape(self.nVertexPerCircle*2))
            return l
            
    def render(self):
        for i,b in enumerate(self.bonusList):
            self.updateVertices(i)
        pyglet.gl.glLineWidth(self.lw)
        self.batch.draw()
        #~ for c in self.listOfLists:
            #~ c[0].draw(pyglet.gl.GL_POLYGON)
            #~ c[1].draw(pyglet.gl.GL_LINE_LOOP)
            #~ c[2].draw(pyglet.gl.GL_LINES)
