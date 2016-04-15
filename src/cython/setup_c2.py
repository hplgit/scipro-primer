# Note: this file does not work, it generates unknown symbol dice6_
# that we avoid with calling f2py directly.

#!/usr/bin/env python
def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    #config = Configuration('packagename',parent_package,top_path)
    config = Configuration(None, parent_package, top_path)
    # Not necessary:
    """
    config.add_library('_dice6_c',
                       sources=['dice6_handwritten.c'])
    config.add_extension('_dice6_c',
                         sources=['dice6_handwritten.pyf'],
                         libraries=['_dice6_c'])
    """
    # This fails: seems to generate dice6_, while direct use
    # of f2py does not (see make_c.sh)
    config.add_extension('_dice6_c',
                         sources=['dice6_handwritten.pyf',
                                  'dice6_handwritten.c'])
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
