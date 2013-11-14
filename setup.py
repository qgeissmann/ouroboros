
from distutils.core import setup, Extension
import numpy
 
module1 = Extension(    'C_AI',\
                        sources = ['AI.c'],\
                        include_dirs = ['/usr/lib/python2.7/site-packages/numpy/core/include/']\
                    )


 
setup (name = 'PackageName',
        version = '1.1',
        description = 'AI functions for Ourobouros',
        ext_modules = [module1])
      #~ 
