ouroboros
=========

A python opengl (pyglet) multiplayer video game, my first python program.

The artificial inteligence is written in `C` so you need to compile the `C` "library":

```
python2 setup.py build
cp build/lib*/C_AI.so .
```
then you can simply run the main:

```
python2 myApp.py
```

Number of AIs, key bindings, penalty scores, size of the game grid and other stuff are configurable in the `myApp.py` file.

Enjoy


