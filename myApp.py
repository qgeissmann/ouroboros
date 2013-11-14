from myWindow import *
from game import *
from player import *
from playerAI import *
from palette import *
import numpy as np
import threading

import pyglet

# left up right down keys
lurd = [\
[pyglet.window.key.LEFT,\
pyglet.window.key.UP,\
pyglet.window.key.RIGHT,\
pyglet.window.key.DOWN],\

[pyglet.window.key.A,\
pyglet.window.key.W,\
pyglet.window.key.D,\
pyglet.window.key.S]\
]\

##DEBUG=
np.random.seed(0)
#~ FPS = 1.0
#~ g = Game(20) 

##NORMAL
FPS = 16.0
fullScreen=True
g = Game(40,nBonus=3) 

palet = [Palette([(64,64,255,200),(72,72,200,200)]), Palette([(255,64,64,200),(200,72,72,200)]) ]
#~ g.addNewPlayer(Player(g,lurd[0],palet[0]))
#~ g.addNewPlayer(Player(g,lurd[1],palet[1]))
#~ g.addNewPlayer(PlayerAI(g,palet[0]))
g.addNewPlayer(PlayerAI(g,palet[1]))
g.addNewPlayer(PlayerAI(g,palet[0]))
#~ g.addNewPlayer(PlayerAI(g,palet[1]))

#~ g.playLoop(1)

pyglet.clock.schedule_interval(g.playOnce,1/FPS)
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
template=pyglet.gl.Config(alpha_size=8, double_buffer = True)
config = screen.get_best_config(template)
context = config.create_context(None)
w = MyWindow(g,context,FS = fullScreen)
pyglet.app.run()
