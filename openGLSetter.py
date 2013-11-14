from  pyglet import gl
from  pyglet import graphics as gr

ANTI_ALIAS = 0

class OpenGLSetter:
    def __ini__(self):
        pass
    def setGL(self,cte):
        if cte == ANTI_ALIAS:
            gl.glEnable( gl.GL_BLEND)
            #~ gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE, gl.GL_ONE);
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            #~ gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE, gl.GL_ONE);
            #~ gl.glEnable( gl.GL_MULTISAMPLE ); 
            

            #~ gl.glEnable(gl.GL_LINE_SMOOTH);
            #~ ;
            
            gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST);
            gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST);

            pass
    
#~ class GL_Group_SegmentFill(gr.Group):
#~ class GL_Group_SegmentFill(gr.Group):
    #~ def set_state(self):
        gl.glDisable(gl.GL_POLYGON_SMOOTH)
        
      
