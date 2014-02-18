from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name='Monte Carlo simulation',
  ext_modules=[Extension('_dice6_cy', ['dice6.pyx'],)],
  cmdclass={'build_ext': build_ext},
)
