from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sources = ['dice6_cwrap.pyx', 'dice6_c.c']

setup(
  name='Monte Carlo simulation',
  ext_modules=[Extension('_dice6_c2', sources)],
  cmdclass={'build_ext': build_ext},
)
