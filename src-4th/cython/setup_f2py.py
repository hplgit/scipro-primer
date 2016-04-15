from numpy.distutils.core import Extension, setup

setup(
    name='...',
    ext_modules=[
        Extension(name='_dice6_c1',
                  sources=['dice6_c.pyf',
                           'dice6_f.c'])]
    )
