from numpy import linspace, sin, cos, pi, array, asarray, ndarray, sqrt, abs
import pprint, copy, glob, os
from math import radians

from MatplotlibDraw import MatplotlibDraw
drawing_tool = MatplotlibDraw()

def point(x, y, check_inside=False):
    for obj, name in zip([x, y], ['x', 'y']):
        if isinstance(obj, (float,int)):
            pass
        elif isinstance(obj, ndarray):
            if obj.size == 1:
                pass
            else:
                raise TypeError('%s=%s of type %d has length=%d > 1' %
                                (name, obj, type(obj), obj.size))
        else:
            raise TypeError('%s=%s is of wrong type %d' %
                            (name, obj, type(obj)))
    if check_inside:
        ok, msg = drawing_tool.inside((x,y), exception=True)
        if not ok:
            print msg

    return array((x, y), dtype=float)

def distance(p1, p2):
    p1 = arr2D(p1);  p2 = arr2D(p2)
    d = p2 - p1
    return sqrt(d[0]**2 + d[1]**2)

def unit_vec(x, y=None):
    """Return unit vector of the vector (x,y), or just x if x is a 2D point."""
    if isinstance(x, (float,int)) and isinstance(y, (float,int)):
        x = point(x, y)
    elif isinstance(x, (list,tuple,ndarray)) and y is None:
        return arr2D(x)/sqrt(x[0]**2 + x[1]**2)
    else:
        raise TypeError('x=%s is %s, must be float or ndarray 2D point' %
                        (x, type(x)))

def arr2D(x, check_inside=False):
    if isinstance(x, (tuple,list,ndarray)):
        if len(x) == 2:
            pass
        else:
            raise ValueError('x=%s has length %d, not 2' % (x, len(x)))
    else:
        raise TypeError('x=%s must be list/tuple/ndarray, not %s' %
                        (x, type(x)))
    if check_inside:
        ok, msg = drawing_tool.inside(x, exception=True)
        if not ok:
            print msg

    return asarray(x, dtype=float)

def _is_sequence(seq, length=None,
                 can_be_None=False, error_message=True):
    if can_be_None:
        legal_types = (list,tuple,ndarray,None)
    else:
        legal_types = (list,tuple,ndarray)

    if isinstance(seq, legal_types):
        if length is not None:
            if length == len(seq):
                return True
            elif error_message:
                raise TypeError('%s is %s; must be %s of length %d' %
                            (str(seq), type(seq),
                            ', '.join([str(t) for t in legal_types]),
                             len(seq)))
            else:
                return False
        else:
            return True
    elif error_message:
        raise TypeError('%s is %s, %s; must be %s' %
                        (str(seq), seq.__class__.__name__, type(seq),
                        ','.join([str(t)[5:-1] for t in legal_types])))
    else:
        return False

def is_sequence(*sequences, **kwargs):
    length = kwargs.get('length', 2)
    can_be_None = kwargs.get('can_be_None', False)
    error_message = kwargs.get('error_message', True)
    check_inside = kwargs.get('check_inside', False)
    for x in sequences:
        _is_sequence(x, length=length, can_be_None=can_be_None,
                     error_message=error_message)
        if check_inside:
            ok, msg = drawing_tool.inside(x, exception=True)
            if not ok:
                print msg


def animate(fig, time_points, action, moviefiles=False,
            pause_per_frame=0.5, **action_kwargs):
    if moviefiles:
        # Clean up old frame files
        framefilestem = 'tmp_frame_'
        framefiles = glob.glob('%s*.png' % framefilestem)
        for framefile in framefiles:
            os.remove(framefile)

    for n, t in enumerate(time_points):
        drawing_tool.erase()

        action(t, fig, **action_kwargs)
        #could demand returning fig, but in-place modifications
        #are done anyway
        #fig = action(t, fig)
        #if fig is None:
        #    raise TypeError(
        #        'animate: action returns None, not fig\n'
        #        '(a Shape object with the whole figure)')

        fig.draw()
        drawing_tool.display()

        if moviefiles:
            drawing_tool.savefig('%s%04d.png' % (framefilestem, n))

    if moviefiles:
        return '%s%%04d.png' % framefilestem


class Shape:
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """
    def __init__(self):
        """
        Never to be called from subclasses.
        """
        raise NotImplementedError(
            'class %s must implement __init__,\nwhich defines '
            'self.shapes as a dict (or list) of Shape objects\n'
            'Do not call Shape.__init__!' % \
            self.__class__.__name__)

    def set_name(self, name):
        self.name = name
        return self

    def get_name(self):
        return self.name if hasattr(self, 'name') else 'no_name'

    def __iter__(self):
        # We iterate over self.shapes many places, and will
        # get here if self.shapes is just a Shape object and
        # not the assumed dict/list.
        print 'Warning: class %s does not define self.shapes\n'\
              'as a dict of Shape objects'
        return [self]  # Make the iteration work

    def copy(self):
        return copy.deepcopy(self)

    def __getitem__(self, name):
        """
        Allow indexing like::

           obj1['name1']['name2']

        all the way down to ``Curve`` or ``Point`` (``Text``)
        objects.
        """
        if hasattr(self, 'shapes'):
            if name in self.shapes:
                return self.shapes[name]
            else:
                for shape in self.shapes:
                    if isinstance(self.shapes[shape], (Curve,Point)):
                        # Indexing of Curve/Point/Text is not possible
                        raise TypeError(
                            'Index "%s" (%s) is illegal' %
                            (name, self.__class__.__name__))
                    return self.shapes[shape][name]
        else:
            raise Exception('This is a bug')


    def _for_all_shapes(self, func, *args, **kwargs):
        if not hasattr(self, 'shapes'):
            # When self.shapes is lacking, we either come to
            # a special implementation of func or we come here
            # because Shape.func is just inherited. This is
            # an error if the class is not Curve or Point
            if isinstance(self, (Curve, Point)):
                return  # ok: no shapes and no func
            else:
                raise AttributeError('class %s has no shapes attribute!' %
                                     self.__class__.__name__)

        is_dict = True if isinstance(self.shapes, dict) else False
        for k, shape in enumerate(self.shapes):
            if is_dict:
                shape_name = shape
                shape = self.shapes[shape]
            else:
                shape_name = k  # use index as name if list

            if not isinstance(shape, Shape):
                if isinstance(shape, dict):
                    raise TypeError(
                        'class %s has a self.shapes member "%s" that is just\n'
                        'a plain dictionary,\n%s\n'
                        'Did you mean to embed this dict in a Composition\n'
                        'object?' % (self.__class__.__name__, shape_name,
                        str(shape)))
                elif isinstance(shape, (list,tuple)):
                    raise TypeError(
                        'class %s has self.shapes member "%s" containing\n'
                        'a %s object %s,\n'
                        'Did you mean to embed this list in a Composition\n'
                        'object?' % (self.__class__.__name__, shape_name,
                        type(shape), str(shape)))
                elif shape is None:
                    raise TypeError(
                        'class %s has a self.shapes member "%s" that is None.\n'
                        'Some variable name is wrong, or some function\n'
                        'did not return the right object...' \
                        % (self.__class__.__name__, shape_name))
                else:
                    raise TypeError(
                        'class %s has a self.shapes member "%s" of %s which '
                        'is not a Shape object\n%s' %
                        (self.__class__.__name__, shape_name, type(shape),
                         pprint.pformat(self.shapes)))

            if isinstance(shape, Curve):
                shape.name = shape_name
            getattr(shape, func)(*args, **kwargs)

    def draw(self):
        self._for_all_shapes('draw')
        return self

    def draw_dimensions(self):
        if hasattr(self, 'dimensions'):
            for shape in self.dimensions:
                self.dimensions[shape].draw()
            return self
        else:
            #raise AttributeError('no self.dimensions dict for defining dimensions of class %s' % self.__classname__.__name__)
            return self

    def rotate(self, angle, center):
        is_sequence(center, length=2)
        self._for_all_shapes('rotate', angle, center)
        return self

    def translate(self, vec):
        is_sequence(vec, length=2)
        self._for_all_shapes('translate', vec)
        return self

    def scale(self, factor):
        self._for_all_shapes('scale', factor)
        return self

    def deform(self, displacement_function):
        self._for_all_shapes('deform', displacement_function)
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': 1E+20, 'xmax': -1E+20,
                      'ymin': 1E+20, 'ymax': -1E+20}
        self._for_all_shapes('minmax_coordinates', minmax)
        return minmax

    def recurse(self, name, indent=0):
        if not isinstance(self.shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self.shapes))
        space = ' '*indent
        print space, '%s: %s.shapes has entries' % \
              (self.__class__.__name__, name), \
              str(list(self.shapes.keys()))[1:-1]

        for shape in self.shapes:
            print space,
            print 'call %s.shapes["%s"].recurse("%s", %d)' % \
                  (name, shape, shape, indent+2)
            self.shapes[shape].recurse(shape, indent+2)

    def graphviz_dot(self, name, classname=True):
        if not isinstance(self.shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self.shapes))
        dotfile = name + '.dot'
        pngfile = name + '.png'
        if classname:
            name = r"%s:\n%s" % (self.__class__.__name__, name)

        couplings = self._object_couplings(name, classname=classname)
        # Insert counter for similar names
        from collections import defaultdict
        count = defaultdict(lambda: 0)
        couplings2 = []
        for i in range(len(couplings)):
            parent, child = couplings[i]
            count[child] += 1
            parent += ' (%d)' % count[parent]
            child += ' (%d)' % count[child]
            couplings2.append((parent, child))
        print 'graphviz', couplings, count
        # Remove counter for names there are only one of
        for i in range(len(couplings)):
            parent2, child2 = couplings2[i]
            parent, child = couplings[i]
            if count[parent] > 1:
                parent = parent2
            if count[child] > 1:
                child = child2
            couplings[i] = (parent, child)
        print couplings
        f = open(dotfile, 'w')
        f.write('digraph G {\n')
        for parent, child in couplings:
            f.write('"%s" -> "%s";\n' % (parent, child))
        f.write('}\n')
        f.close()
        print 'Run dot -Tpng -o %s %s' % (pngfile, dotfile)

    def _object_couplings(self, parent, couplings=[], classname=True):
        """Find all couplings of parent and child objects in a figure."""
        for shape in self.shapes:
            if classname:
                childname = r"%s:\n%s" % \
                            (self.shapes[shape].__class__.__name__, shape)
            else:
                childname = shape
            couplings.append((parent, childname))
            self.shapes[shape]._object_couplings(childname, couplings,
                                                 classname)
        return couplings


    def set_linestyle(self, style):
        styles = ('solid', 'dashed', 'dashdot', 'dotted')
        if style not in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_linestyle:',
                              style, str(styles)))
        self._for_all_shapes('set_linestyle', style)
        return self

    def set_linewidth(self, width):
        if not isinstance(width, int) and width >= 0:
            raise ValueError('%s: width=%s must be positive integer' %
                             (self.__class__.__name__ + '.set_linewidth:',
                              width))
        self._for_all_shapes('set_linewidth', width)
        return self

    def set_linecolor(self, color):
        if color in drawing_tool.line_colors:
            color = drawing_tool.line_colors[color]
        elif color in drawing_tool.line_colors.values():
            pass # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_linecolor:',
                                 color, list(drawing_tool.line_colors.keys())))
        self._for_all_shapes('set_linecolor', color)
        return self

    def set_arrow(self, style):
        styles = ('->', '<-', '<->')
        if not style in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_arrow:',
                              style, styles))
        self._for_all_shapes('set_arrow', style)
        return self

    def set_filled_curves(self, color='', pattern=''):
        if color in drawing_tool.line_colors:
            color = drawing_tool.line_colors[color]
        elif color in drawing_tool.line_colors.values():
            pass # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_filled_curves:',
                              color, list(drawing_tool.line_colors.keys())))
        self._for_all_shapes('set_filled_curves', color, pattern)
        return self

    def set_shadow(self, pixel_displacement=3):
        self._for_all_shapes('set_shadow', pixel_displacement)
        return self

    def show_hierarchy(self, indent=0, format='std'):
        """Recursive pretty print of hierarchy of objects."""
        if not isinstance(self.shapes, dict):
            print 'cannot print hierarchy when %s.shapes is not a dict' % \
                  self.__class__.__name__
        s = ''
        if format == 'dict':
            s += '{'
        for shape in self.shapes:
            if format == 'dict':
                shape_str = repr(shape) + ':'
            elif format == 'plain':
                shape_str = shape
            else:
                shape_str = shape + ':'
            if format == 'dict' or format == 'plain':
                class_str = ''
            else:
                class_str = ' (%s)' % \
                            self.shapes[shape].__class__.__name__
            s += '\n%s%s%s %s' % (
                ' '*indent,
                shape_str,
                class_str,
                self.shapes[shape].show_hierarchy(indent+4, format))

        if format == 'dict':
            s += '}'
        return s

    def __str__(self):
        """Display hierarchy with minimum information (just object names)."""
        return self.show_hierarchy(format='plain')

    def __repr__(self):
        """Display hierarchy as a dictionary."""
        return self.show_hierarchy(format='dict')
        #return pprint.pformat(self.shapes)


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes."""
    def __init__(self, x, y):
        """
        `x`, `y`: arrays holding the coordinates of the curve.
        """
        self.x = asarray(x, dtype=float)
        self.y = asarray(y, dtype=float)
        #self.shapes must not be defined in this class
        #as self.shapes holds children objects:
        #Curve has no children (end leaf of self.shapes tree)

        self.linestyle = None
        self.linewidth = None
        self.linecolor = None
        self.fillcolor = None
        self.fillpattern = None
        self.arrow = None
        self.shadow = False
        self.name = None  # name of object that this Curve represents

    def inside_plot_area(self, verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        xmin, xmax = self.x.min(), self.x.max()
        ymin, ymax = self.y.min(), self.y.max()
        t = drawing_tool
        inside = True
        if xmin < t.xmin:
            inside = False
            if verbose:
                print 'x_min=%g < plot area x_min=%g' % (xmin, t.xmin)
        if xmax > t.xmax:
            inside = False
            if verbose:
                print 'x_max=%g > plot area x_max=%g' % (xmax, t.xmax)
        if ymin < t.ymin:
            inside = False
            if verbose:
                print 'y_min=%g < plot area y_min=%g' % (ymin, t.ymin)
        if ymax > t.ymax:
            inside = False
            if verbose:
                print 'y_max=%g > plot area y_max=%g' % (ymax, t.ymax)
        return inside

    def draw(self):
        """
        Send the curve to the plotting engine. That is, convert
        coordinate information in self.x and self.y, together
        with optional settings of linestyles, etc., to
        plotting commands for the chosen engine.
        """
        self.inside_plot_area()
        drawing_tool.plot_curve(
            self.x, self.y,
            self.linestyle, self.linewidth, self.linecolor,
            self.arrow, self.fillcolor, self.fillpattern,
            self.shadow, self.name)

    def rotate(self, angle, center):
        """
        Rotate all coordinates: `angle` is measured in degrees and
        (`x`,`y`) is the "origin" of the rotation.
        """
        angle = radians(angle)
        x, y = center
        c = cos(angle);  s = sin(angle)
        xnew = x + (self.x - x)*c - (self.y - y)*s
        ynew = y + (self.x - x)*s + (self.y - y)*c
        self.x = xnew
        self.y = ynew
        return self

    def scale(self, factor):
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        self.x = factor*self.x
        self.y = factor*self.y
        return self

    def translate(self, vec):
        """Translate all coordinates by a vector `vec`."""
        self.x += vec[0]
        self.y += vec[1]
        return self

    def deform(self, displacement_function):
        """Displace all coordinates according to displacement_function(x,y)."""
        for i in range(len(self.x)):
            self.x[i], self.y[i] = displacement_function(self.x[i], self.y[i])
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': [], 'xmax': [], 'ymin': [], 'ymax': []}
        minmax['xmin'] = min(self.x.min(), minmax['xmin'])
        minmax['xmax'] = max(self.x.max(), minmax['xmax'])
        minmax['ymin'] = min(self.y.min(), minmax['ymin'])
        minmax['ymax'] = max(self.y.max(), minmax['ymax'])
        return minmax

    def recurse(self, name, indent=0):
        space = ' '*indent
        print space, 'reached "bottom" object %s' % \
              self.__class__.__name__

    def _object_couplings(self, parent, couplings=[], classname=True):
        return

    def set_linecolor(self, color):
        self.linecolor = color
        return self

    def set_linewidth(self, width):
        self.linewidth = width
        return self

    def set_linestyle(self, style):
        self.linestyle = style
        return self

    def set_arrow(self, style=None):
        self.arrow = style
        return self

    def set_filled_curves(self, color='', pattern=''):
        self.fillcolor = color
        self.fillpattern = pattern
        return self

    def set_shadow(self, pixel_displacement=3):
        self.shadow = pixel_displacement
        return self

    def show_hierarchy(self, indent=0, format='std'):
        if format == 'dict':
            return '"%s"' % str(self)
        elif format == 'plain':
            return ''
        else:
            return str(self)

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = '%d coords' % self.x.size
        if not self.inside_plot_area(verbose=False):
            s += ', some coordinates are outside plotting area!\n'
        props = ('linecolor', 'linewidth', 'linestyle', 'arrow',
                 'fillcolor', 'fillpattern')
        for prop in props:
            value = getattr(self, prop)
            if value is not None:
                s += ' %s=%s' % (prop, repr(value))
        return s

    def __repr__(self):
        return str(self)


class Spline(Shape):
    # Note: UnivariateSpline interpolation may not work if
    # the x[i] points are far from uniformly spaced
    def __init__(self, x, y, degree=3, resolution=501):
        from scipy.interpolate import UnivariateSpline
        self.smooth = UnivariateSpline(x, y, s=0, k=degree)
        self.xcoor = linspace(x[0], x[-1], resolution)
        ycoor = self.smooth(self.xcoor)
        self.shapes = {'smooth': Curve(self.xcoor, ycoor)}

    def geometric_features(self):
        s = self.shapes['smooth']
        return {'start': point(s.x[0], s.y[0]),
                'end': point(s.x[-1], s.y[-1]),
                'interval': [s.x[0], s.x[-1]]}

    def __call__(self, x):
        return self.smooth(x)

    # Can easily find the derivative and the integral as
    # self.smooth.derivative(n=1) and self.smooth.antiderivative()




class SketchyFunc1(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [1, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=1, xmax=6, ymin=2.4, ymax=5):
        x = array([1, 2,   3,   4, 5,   6])
        y = array([5, 3.5, 3.8, 3, 2.5, 2.4])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc3(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [0, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=0, xmax=6, ymin=0.5, ymax=3.8):
        x = array([0, 2,   3,   4, 5,   6])
        #y = array([2, 3.5, 3.8, 2, 2.5, 2.6])
        y = array([0.5, 3.5, 3.8, 2, 2.5, 3.5])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc4(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    Can be a companion function to SketchyFunc3.
    """
    domain = [1, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=0, xmax=6, ymin=0.5, ymax=1.8):
        x = array([0, 2,   3,   4, 5,   6])
        y = array([1.5, 1.3, 0.7, 0.5, 0.6, 0.8])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc2(Shape):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [0, 2.25]
    def __init__(self, name=None, name_pos='end',
                 xmin=0, xmax=2.25, ymin=0.046679703125, ymax=1.259375):

        a = 0; b = 2.25
        resolution = 100
        x = linspace(a, b, resolution+1)
        f = self  # for calling __call__
        y = f(x)
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        self.shapes = {'smooth': Curve(x, y)}
        self.shapes['smooth'].set_linecolor('black')

        pos = point(a, f(a)) if name_pos == 'start' else point(b, f(b))
        if name is not None:
            self.shapes['name'] = Text(name, pos + point(0,0.1))

    def __call__(self, x):
        return 0.5+x*(2-x)*(0.9-x) # on [0, 2.25]

class Point(Shape):
    """A point (x,y) which can be rotated, translated, and scaled."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        #self.shapes is not needed in this class

    def __add__(self, other):
        if isinstance(other, (list,tuple)):
            other = Point(other)
        return Point(self.x+other.x, self.y+other.y)

    # class Point is an abstract class - only subclasses are useful
    # and must implement draw
    def draw(self):
        raise NotImplementedError(
            'class %s must implement the draw method' %
            self.__class__.__name__)

    def rotate(self, angle, center):
        """Rotate point an `angle` (in degrees) around (`x`,`y`)."""
        angle = angle*pi/180
        x, y = center
        c = cos(angle);  s = sin(angle)
        xnew = x + (self.x - x)*c - (self.y - y)*s
        ynew = y + (self.x - x)*s + (self.y - y)*c
        self.x = xnew
        self.y = ynew
        return self

    def scale(self, factor):
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        self.x = factor*self.x
        self.y = factor*self.y
        return self

    def translate(self, vec):
        """Translate point by a vector `vec`."""
        self.x += vec[0]
        self.y += vec[1]
        return self

    def deform(self, displacement_function):
        """Displace coordinates according to displacement_function(x,y)."""
        for i in range(len(self.x)):
            self.x, self.y = displacement_function(self.x, self.y)
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': [], 'xmax': [], 'ymin': [], 'ymax': []}
        minmax['xmin'] = min(self.x, minmax['xmin'])
        minmax['xmax'] = max(self.x, minmax['xmax'])
        minmax['ymin'] = min(self.y, minmax['ymin'])
        minmax['ymax'] = max(self.y, minmax['ymax'])
        return minmax

    def recurse(self, name, indent=0):
        space = ' '*indent
        print space, 'reached "bottom" object %s' % \
              self.__class__.__name__

    def _object_couplings(self, parent, couplings=[], classname=True):
        return

    # No need for set_linecolor etc since self._for_all_shapes, which
    # is always called for these functions, makes a test and stops
    # calls if self.shapes is missing and the object is Point or Curve

    def show_hierarchy(self, indent=0, format='std'):
        s = '%s at (%g,%g)' % (self.__class__.__name__, self.x, self.y)
        if format == 'dict':
            return '"%s"' % s
        elif format == 'plain':
            return ''
        else:
            return s

# no need to store input data as they are invalid after rotations etc.
class Rectangle(Shape):
    """
    Rectangle specified by the point `lower_left_corner`, `width`,
    and `height`.
    """
    def __init__(self, lower_left_corner, width, height):
        is_sequence(lower_left_corner)
        p = arr2D(lower_left_corner)  # short form
        x = [p[0], p[0] + width,
             p[0] + width, p[0], p[0]]
        y = [p[1], p[1], p[1] + height,
             p[1] + height, p[1]]
        self.shapes = {'rectangle': Curve(x,y)}

        # Dimensions
        dims = {
            'width': Distance_wText(p + point(0, -height/5.),
                                    p + point(width, -height/5.),
                                    'width'),
            'height': Distance_wText(p + point(width + width/5., 0),
                                     p + point(width + width/5., height),
                                   'height'),
            'lower_left_corner': Text_wArrow('lower_left_corner',
                                             p - point(width/5., height/5.), p)
            }
        self.dimensions = dims

    def geometric_features(self):
        """
        Return dictionary with

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        lower_left           Lower left corner point.
        upper_left           Upper left corner point.
        lower_right          Lower right corner point.
        upper_right          Upper right corner point.
        lower_mid            Middle point on lower side.
        upper_mid            Middle point on upper side.
        center               Center point
        ==================== =============================================
        """
        r = self.shapes['rectangle']
        d = {'lower_left': point(r.x[0], r.y[0]),
             'lower_right': point(r.x[1], r.y[1]),
             'upper_right': point(r.x[2], r.y[2]),
             'upper_left': point(r.x[3], r.y[3])}
        d['lower_mid'] = 0.5*(d['lower_left'] + d['lower_right'])
        d['upper_mid'] = 0.5*(d['upper_left'] + d['upper_right'])
        d['left_mid'] = 0.5*(d['lower_left'] + d['upper_left'])
        d['right_mid'] = 0.5*(d['lower_right'] + d['upper_right'])
        d['center'] = point(d['lower_mid'][0], d['left_mid'][1])
        return d

class Triangle(Shape):
    """
    Triangle defined by its three vertices p1, p2, and p3.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    p1, p2, p3           Corners as given to the constructor.
    ==================== =============================================

    """
    def __init__(self, p1, p2, p3):
        is_sequence(p1, p2, p3)
        x = [p1[0], p2[0], p3[0], p1[0]]
        y = [p1[1], p2[1], p3[1], p1[1]]
        self.shapes = {'triangle': Curve(x,y)}

        # Dimensions
        self.dimensions = {'p1': Text('p1', p1),
                           'p2': Text('p2', p2),
                           'p3': Text('p3', p3)}

    def geometric_features(self):
        t = self.shapes['triangle']
        return {'p1': point(t.x[0], t.y[0]),
                'p2': point(t.x[1], t.y[1]),
                'p3': point(t.x[2], t.y[2])}

class Line(Shape):
    def __init__(self, start, end):
        is_sequence(start, end, length=2)
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        self.shapes = {'line': Curve(x, y)}

    def geometric_features(self):
        line = self.shapes['line']
        return {'start': point(line.x[0], line.y[0]),
                'end': point(line.x[1], line.y[1]),}

    def compute_formulas(self):
        x, y = self.shapes['line'].x, self.shapes['line'].y

        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        try:
            self.a = (y[1] - y[0])/(x[1] - x[0])
            self.b = y[0] - self.a*x[0]
        except ZeroDivisionError:
            # Vertical line, y is not a function of x
            self.a = None
            self.b = None
        try:
            if self.a is None:
                self.c = 0
            else:
                self.c = 1/float(self.a)
            if self.b is None:
                self.d = x[1]
        except ZeroDivisionError:
            # Horizontal line, x is not a function of y
            self.c = None
            self.d = None

    def compute_formulas(self):
        x, y = self.shapes['line'].x, self.shapes['line'].y

        tol = 1E-14
        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        if abs(x[1] - x[0]) > tol:
            self.a = (y[1] - y[0])/(x[1] - x[0])
            self.b = y[0] - self.a*x[0]
        else:
            # Vertical line, y is not a function of x
            self.a = None
            self.b = None
        if self.a is None:
            self.c = 0
        elif abs(self.a) > tol:
            self.c = 1/float(self.a)
            self.d = x[1]
        else:  # self.a is 0
            # Horizontal line, x is not a function of y
            self.c = None
            self.d = None

    def __call__(self, x=None, y=None):
        """Given x, return y on the line, or given y, return x."""
        self.compute_formulas()
        if x is not None and self.a is not None:
            return self.a*x + self.b
        elif y is not None and self.c is not None:
            return self.c*y + self.d
        else:
            raise ValueError(
                'Line.__call__(x=%s, y=%s) not meaningful' % \
                (x, y))

    def new_interval(self, x=None, y=None):
        """Redefine current Line to cover interval in x or y."""
        if x is not None:
            is_sequence(x, length=2)
            xL, xR = x
            new_line = Line((xL, self(x=xL)), (xR, self(x=xR)))
        elif y is not None:
            is_sequence(y, length=2)
            yL, yR = y
            new_line = Line((xL, self(y=xL)), (xR, self(y=xR)))
        self.shapes['line'] = new_line['line']
        return self


# First implementation of class Circle
class Circle(Shape):
    def __init__(self, center, radius, resolution=180):
        self.center, self.radius = center, radius
        self.resolution = resolution

        t = linspace(0, 2*pi, resolution+1)
        x0 = center[0];  y0 = center[1]
        R = radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        self.shapes = {'circle': Curve(x, y)}

    def __call__(self, theta):
        """
        Return (x, y) point corresponding to angle theta.
        Not valid after a translation, rotation, or scaling.
        """
        return self.center[0] + self.radius*cos(theta), \
               self.center[1] + self.radius*sin(theta)


class Arc(Shape):
    def __init__(self, center, radius,
                 start_angle, arc_angle,
                 resolution=180):
        is_sequence(center)

        # Must record some parameters for __call__
        self.center = arr2D(center)
        self.radius = radius
        self.start_angle = radians(start_angle)
        self.arc_angle = radians(arc_angle)

        t = linspace(self.start_angle,
                     self.start_angle + self.arc_angle,
                     resolution+1)
        x0 = center[0];  y0 = center[1]
        R = radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        self.shapes = {'arc': Curve(x, y)}

        # Cannot set dimensions (Arc_wText recurses into this
        # constructor forever). Set in test_Arc instead.

        # Stored geometric features
    def geometric_features(self):
        a = self.shapes['arc']
        m = len(a.x)/2  # mid point in array
        d = {'start': point(a.x[0], a.y[0]),
             'end': point(a.x[-1], a.y[-1]),
             'mid': point(a.x[m], a.y[m])}
        return d

    def __call__(self, theta):
        """
        Return (x,y) point at start_angle + theta.
        Not valid after translation, rotation, or scaling.
        """
        theta = radians(theta)
        t = self.start_angle + theta
        x0 = self.center[0]
        y0 = self.center[1]
        R = self.radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        return (x, y)

# Alternative for small arcs: Parabola

class Parabola(Shape):
    def __init__(self, start, mid, stop, resolution=21):
        self.p1, self.p2, self.p3 = start, mid, stop

        # y as function of x? (no point on line x=const?)
        tol = 1E-14
        if abs(self.p1[0] - self.p2[0]) > 1E-14 and \
           abs(self.p2[0] - self.p3[0]) > 1E-14 and \
           abs(self.p3[0] - self.p1[0]) > 1E-14:
            self.y_of_x = True
        else:
            self.y_of_x = False
        # x as function of y? (no point on line y=const?)
        tol = 1E-14
        if abs(self.p1[1] - self.p2[1]) > 1E-14 and \
           abs(self.p2[1] - self.p3[1]) > 1E-14 and \
           abs(self.p3[1] - self.p1[1]) > 1E-14:
            self.x_of_y = True
        else:
            self.x_of_y = False

        if self.y_of_x:
            x = linspace(start[0], end[0], resolution)
            y = self(x=x)
        elif self.x_of_y:
            y = linspace(start[1], end[1], resolution)
            x = self(y=y)
        else:
            raise ValueError(
                'Parabola: two or more points lie on x=const '
                'or y=const - not allowed')
        self.shapes = {'parabola': Curve(x, y)}

    def __call__(self, x=None, y=None):
        if x is not None and self.y_of_x:
            return self._L2x(self.p1, self.p2)*self.p3[1] + \
                   self._L2x(self.p2, self.p3)*self.p1[1] + \
                   self._L2x(self.p3, self.p1)*self.p2[1]
        elif y is not None and self.x_of_y:
            return self._L2y(self.p1, self.p2)*self.p3[0] + \
                   self._L2y(self.p2, self.p3)*self.p1[0] + \
                   self._L2y(self.p3, self.p1)*self.p2[0]
        else:
            raise ValueError(
                'Parabola.__call__(x=%s, y=%s) not meaningful' % \
                (x, y))

    def _L2x(self, x, pi, pj, pk):
        return (x - pi[0])*(x - pj[0])/((pk[0] - pi[0])*(pk[0] - pj[0]))

    def _L2y(self, y, pi, pj, pk):
        return (y - pi[1])*(y - pj[1])/((pk[1] - pi[1])*(pk[1] - pj[1]))


class Circle(Arc):
    def __init__(self, center, radius, resolution=180):
        Arc.__init__(self, center, radius, 0, 360, resolution)


class Wall(Shape):
    def __init__(self, x, y, thickness, pattern='/', transparent=False):
        is_sequence(x, y, length=len(x))
        if isinstance(x[0], (tuple,list,ndarray)):
            # x is list of curves
            x1 = concatenate(x)
        else:
            x1 = asarray(x, float)
        if isinstance(y[0], (tuple,list,ndarray)):
            # x is list of curves
            y1 = concatenate(y)
        else:
            y1 = asarray(y, float)
        self.x1 = x1;  self.y1 = y1

        # Displaced curve (according to thickness)
        x2 = x1
        y2 = y1 + thickness
        # Combine x1,y1 with x2,y2 reversed
        from numpy import concatenate
        x = concatenate((x1, x2[-1::-1]))
        y = concatenate((y1, y2[-1::-1]))
        wall = Curve(x, y)
        wall.set_filled_curves(color='white', pattern=pattern)
        x = [x1[-1]] + x2[-1::-1].tolist() + [x1[0]]
        y = [y1[-1]] + y2[-1::-1].tolist() + [y1[0]]
        self.shapes = {'wall': wall}

        from collections import OrderedDict
        self.shapes = OrderedDict()
        self.shapes['wall'] = wall
        if transparent:
            white_eraser = Curve(x, y)
            white_eraser.set_linecolor('white')
            self.shapes['eraser'] = white_eraser

    def geometric_features(self):
        d = {'start': point(self.x1[0], self.y1[0]),
             'end': point(self.x1[-1], self.y1[-1])}
        return d

class Wall2(Shape):
    def __init__(self, x, y, thickness, pattern='/'):
        is_sequence(x, y, length=len(x))
        if isinstance(x[0], (tuple,list,ndarray)):
            # x is list of curves
            x1 = concatenate(x)
        else:
            x1 = asarray(x, float)
        if isinstance(y[0], (tuple,list,ndarray)):
            # x is list of curves
            y1 = concatenate(y)
        else:
            y1 = asarray(y, float)

        self.x1 = x1;  self.y1 = y1

        # Displaced curve (according to thickness)
        x2 = x1.copy()
        y2 = y1.copy()

        def displace(idx, idx_m, idx_p):
            # Find tangent and normal
            tangent = point(x1[idx_m], y1[idx_m]) - point(x1[idx_p], y1[idx_p])
            tangent = unit_vec(tangent)
            normal = point(tangent[1], -tangent[0])
            # Displace length "thickness" in "positive" normal direction
            displaced_pt = point(x1[idx], y1[idx]) + thickness*normal
            x2[idx], y2[idx] = displaced_pt

        for i in range(1, len(x1)-1):
            displace(i-1, i+1, i)  # centered difference for normal comp.
        # One-sided differences at the end points
        i = 0
        displace(i, i+1, i)
        i = len(x1)-1
        displace(i-1, i, i)

        # Combine x1,y1 with x2,y2 reversed
        from numpy import concatenate
        x = concatenate((x1, x2[-1::-1]))
        y = concatenate((y1, y2[-1::-1]))
        wall = Curve(x, y)
        wall.set_filled_curves(color='white', pattern=pattern)
        x = [x1[-1]] + x2[-1::-1].tolist() + [x1[0]]
        y = [y1[-1]] + y2[-1::-1].tolist() + [y1[0]]
        self.shapes['wall'] = wall

    def geometric_features(self):
        d = {'start': point(self.x1[0], self.y1[0]),
             'end': point(self.x1[-1], self.y1[-1])}
        return d


class VelocityProfile(Shape):
    def __init__(self, start, height, profile, num_arrows, scaling=1):
        # vx, vy = profile(y)

        shapes = {}
        # Draw left line
        shapes['start line'] = Line(start, (start[0], start[1]+height))

        # Draw velocity arrows
        dy = float(height)/(num_arrows-1)
        x = start[0]
        y = start[1]
        r = profile(y)  # Test on return type
        if not isinstance(r, (list,tuple,ndarray)) and len(r) != 2:
            raise TypeError('VelocityProfile constructor: profile(y) function must return velocity vector (vx,vy), not %s' % type(r))

        for i in range(num_arrows):
            y = start[1] + i*dy
            vx, vy = profile(y)
            if abs(vx) < 1E-8:
                continue
            vx *= scaling
            vy *= scaling
            arr = Arrow1((x,y), (x+vx, y+vy), '->')
            shapes['arrow%d' % i] = arr
        # Draw smooth profile
        xs = []
        ys = []
        n = 100
        dy = float(height)/n
        for i in range(n+2):
            y = start[1] + i*dy
            vx, vy = profile(y)
            vx *= scaling
            vy *= scaling
            xs.append(x+vx)
            ys.append(y+vy)
        shapes['smooth curve'] = Curve(xs, ys)
        self.shapes = shapes


class Arrow1(Shape):
    """Draw an arrow as Line with arrow."""
    def __init__(self, start, end, style='->'):
        arrow = Line(start, end)
        arrow.set_arrow(style)
        # Note:
        self.shapes = {'arrow': arrow}

    def geometric_features(self):
        return self.shapes['arrow'].geometric_features()

class Arrow3(Shape):
    """
    Build a vertical line and arrow head from Line objects.
    Then rotate `rotation_angle`.
    """
    def __init__(self, start, length, rotation_angle=0):
        self.bottom = start
        self.length = length
        self.angle = rotation_angle

        top = (self.bottom[0], self.bottom[1] + self.length)
        main = Line(self.bottom, top)
        #head_length = self.length/8.0
        head_length = drawing_tool.xrange/50.
        head_degrees = radians(30)
        head_left_pt = (top[0] - head_length*sin(head_degrees),
                        top[1] - head_length*cos(head_degrees))
        head_right_pt = (top[0] + head_length*sin(head_degrees),
                         top[1] - head_length*cos(head_degrees))
        head_left = Line(head_left_pt, top)
        head_right = Line(head_right_pt, top)
        head_left.set_linestyle('solid')
        head_right.set_linestyle('solid')
        self.shapes = {'line': main, 'head left': head_left,
                       'head right': head_right}

        # rotate goes through self.shapes so self.shapes
        # must be initialized first
        self.rotate(rotation_angle, start)

    def geometric_features(self):
        return self.shapes['line'].geometric_features()


class Text(Point):
    """
    Place `text` at the (x,y) point `position`, with the given
    fontsize (0 indicates that the default fontsize set in drawing_tool
    is to be used). The text is centered around `position` if `alignment` is
    'center'; if 'left', the text starts at `position`, and if
    'right', the right and of the text is located at `position`.
    """
    def __init__(self, text, position, alignment='center', fontsize=0):
        is_sequence(position)
        is_sequence(position, length=2, can_be_None=True)
        self.text = text
        self.position = position
        self.alignment = alignment
        self.fontsize = fontsize
        Point.__init__(self, position[0], position[1])
        #no need for self.shapes here

    def draw(self):
        drawing_tool.text(self.text, (self.x, self.y),
                          self.alignment, self.fontsize)

    def __str__(self):
        return 'text "%s" at (%g,%g)' % (self.text, self.x, self.y)

    def __repr__(self):
        return str(self)


class Text_wArrow(Text):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """
    def __init__(self, text, position, arrow_tip,
                 alignment='center', fontsize=0):
        is_sequence(arrow_tip, length=2, can_be_None=True)
        is_sequence(position)
        self.arrow_tip = arrow_tip
        Text.__init__(self, text, position, alignment, fontsize)

    def draw(self):
        drawing_tool.text(self.text, self.position,
                          self.alignment, self.fontsize,
                          self.arrow_tip)
    def __str__(self):
        return 'annotation "%s" at (%g,%g) with arrow to (%g,%g)' % \
               (self.text, self.x, self.y,
                self.arrow_tip[0], self.arrow_tip[1])

    def __repr__(self):
        return str(self)


class Axis(Shape):
    def __init__(self, start, length, label,
                 rotation_angle=0, fontsize=0,
                 label_spacing=1./45, label_alignment='left'):
        """
        Draw axis from start with `length` to the right
        (x axis). Place label at the end of the arrow tip.
        Then return `rotation_angle` (in degrees).
        The `label_spacing` denotes the space between the label
        and the arrow tip as a fraction of the length of the plot
        in x direction. With `label_alignment` one can place
        the axis label text such that the arrow tip is to the 'left',
        'right', or 'center' with respect to the text field.
        The `label_spacing` and `label_alignment` parameters can
        be used to fine-tune the location of the label.
        """
        # Arrow is vertical arrow, make it horizontal
        arrow = Arrow3(start, length, rotation_angle=-90)
        arrow.rotate(rotation_angle, start)
        if isinstance(label_spacing, (list,tuple)) and len(label_spacing) == 2:
            x_spacing = drawing_tool.xrange*label_spacing[0]
            y_spacing = drawing_tool.yrange*label_spacing[1]
        elif isinstance(label_spacing, (int,float)):
            # just x spacing
            x_spacing = drawing_tool.xrange*label_spacing
            y_spacing = 0
        # should increase spacing for downward pointing axis
        label_pos = [start[0] + length + x_spacing, start[1] + y_spacing]
        label = Text(label, position=label_pos, fontsize=fontsize)
        label.rotate(rotation_angle, start)
        self.shapes = {'arrow': arrow, 'label': label}

    def geometric_features(self):
        return self.shapes['arrow'].geometric_features()

# Maybe Axis3 with label below/above?

class Force(Arrow1):
    """
    Indication of a force by an arrow and a text (symbol).  Draw an
    arrow, starting at `start` and with the tip at `end`.  The symbol
    is placed at `text_pos`, which can be 'start', 'end' or the
    coordinates of a point. If 'end' or 'start', the text is placed at
    a distance `text_spacing` times the width of the total plotting
    area away from the specified point.
    """
    def __init__(self, start, end, text, text_spacing=1./60,
                 fontsize=0, text_pos='start', text_alignment='center'):
        Arrow1.__init__(self, start, end, style='->')
        spacing = drawing_tool.xrange*text_spacing
        start, end = arr2D(start), arr2D(end)

        # Two cases: label at bottom of line or top, need more
        # spacing if bottom
        downward = (end-start)[1] < 0
        upward = not downward  # for easy code reading

        if isinstance(text_pos, str):
            if text_pos == 'start':
                spacing_dir = unit_vec(start - end)
                if upward:
                    spacing *= 1.7
                text_pos = start + spacing*spacing_dir
            elif text_pos == 'end':
                spacing_dir = unit_vec(end - start)
                if downward:
                    spacing *= 1.7
                text_pos = end + spacing*spacing_dir
        self.shapes['text'] = Text(text, text_pos, fontsize=fontsize,
                                   alignment=text_alignment)

    def geometric_features(self):
        d = Arrow1.geometric_features(self)
        d['symbol_location'] = self.shapes['text'].position
        return d

class Axis2(Force):
    def __init__(self, start, length, label,
                 rotation_angle=0, fontsize=0,
                 label_spacing=1./45, label_alignment='left'):
        direction = point(cos(radians(rotation_angle)),
                          sin(radians(rotation_angle)))
        Force.__init__(start=start, end=length*direction, text=label,
                       text_spacing=label_spacing,
                       fontsize=fontsize, text_pos='end',
                       text_alignment=label_alignment)
        # Substitute text by label for axis
        self.shapes['label'] = self.shapes['text']
        del self.shapes['text']

    # geometric features from Force is ok

class Gravity(Axis):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length, fontsize=0):
        Axis.__init__(self, start, length, '$g$', below=False,
                      rotation_angle=-90, label_spacing=1./30,
                      fontsize=fontsize)
        self.shapes['arrow'].set_linecolor('black')


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length, text='$g$', fontsize=0):
        Force.__init__(self, start, (start[0], start[1]-length),
                       text, text_spacing=1./60,
                       fontsize=0, text_pos='end')
        self.shapes['arrow'].set_linecolor('black')


class Distance_wText(Shape):
    """
    Arrow <-> with text (usually a symbol) at the midpoint, used for
    identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).
    """
    def __init__(self, start, end, text, fontsize=0, text_spacing=1/60.,
                 alignment=None, text_pos='mid'):
        start = arr2D(start)
        end   = arr2D(end)

        # Decide first if we have a vertical or horizontal arrow
        vertical = abs(end[0]-start[0]) < 2*abs(end[1]-start[1])

        if vertical:
            # Assume end above start
            if end[1] < start[1]:
                start, end = end, start
            if alignment is None:
                alignment = 'left'
        else:  # horizontal arrow
            # Assume start to the right of end
            if start[0] < end[0]:
                start, end = end, start
            if alignment is None:
                alignment = 'center'

        tangent = end - start
        # Tangeng goes always to the left and upward
        normal = unit_vec([tangent[1], -tangent[0]])
        mid = 0.5*(start + end)  # midpoint of start-end line

        if text_pos == 'mid':
            text_pos = mid + normal*drawing_tool.xrange*text_spacing
            text = Text(text, text_pos, fontsize=fontsize,
                        alignment=alignment)
        else:
            is_sequence(text_pos, length=2)
            text = Text_wArrow(text, text_pos, mid, alignment='left',
                               fontsize=fontsize)
        arrow = Arrow1(start, end, style='<->')
        arrow.set_linecolor('black')
        arrow.set_linewidth(1)
        self.shapes = {'arrow': arrow, 'text': text}

    def geometric_features(self):
        d = self.shapes['arrow'].geometric_features()
        d['text_position'] = self.shapes['text'].position
        return d

class Arc_wText(Shape):
    def __init__(self, text, center, radius,
                 start_angle, arc_angle, fontsize=0,
                 resolution=180, text_spacing=1/60.):
        arc = Arc(center, radius, start_angle, arc_angle,
                  resolution)
        mid = arr2D(arc(arc_angle/2.))
        normal = unit_vec(mid - arr2D(center))
        text_pos = mid + normal*drawing_tool.xrange*text_spacing
        self.shapes = {'arc': arc,
                       'text': Text(text, text_pos, fontsize=fontsize)}

class Composition(Shape):
    def __init__(self, shapes):
        """shapes: list or dict of Shape objects."""
        if isinstance(shapes, (tuple,list)):
            # Convert to dict using the type of the list element as key
            # (add a counter to make the keys unique)
            shapes = {s.__class__.__name__ + '_' + str(i): s
                      for i, s in enumerate(shapes)}
        self.shapes = shapes


# can make help methods: Line.midpoint, Line.normal(pt, dir='left') -> (x,y)

# list annotations in each class? contains extra annotations for explaining
# important parameters to the constructor, e.g., Line.annotations holds
# start and end as Text objects. Shape.demo calls shape.draw and
# for annotation in self.demo: annotation.draw() YES!
# Can make overall demo of classes by making objects and calling demo
# Could include demo fig in each constructor


class SimplySupportedBeam(Shape):
    def __init__(self, pos, size):
        pos = arr2D(pos)
        P0 = (pos[0] - size/2., pos[1]-size)
        P1 = (pos[0] + size/2., pos[1]-size)
        triangle = Triangle(P0, P1, pos)
        gap = size/5.
        h = size/4.  # height of rectangle
        P2 = (P0[0], P0[1]-gap-h)
        rectangle = Rectangle(P2, size, h).set_filled_curves(pattern='/')
        self.shapes = {'triangle': triangle, 'rectangle': rectangle}

        self.dimensions = {'pos': Text('pos', pos),
                           'size': Distance_wText((P2[0], P2[1]-size),
                                                  (P2[0]+size, P2[1]-size),
                                                  'size')}
    def geometric_features(self):
        t = self.shapes['triangle']
        r = self.shapes['rectangle']
        d = {'pos': point(t.x[2], t.y[2]),  # "p2"/pos
             'mid_support': r.geometric_features()['lower_mid']}
        return d


class ConstantBeamLoad(Shape):
    """
    Downward-pointing arrows indicating a vertical load.
    The arrows are of equal length and filling a rectangle
    specified as in the :class:`Rectangle` class.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    mid_point            Middle point at the top of the row of
                         arrows (often used for positioning a text).
    ==================== =============================================
    """
    def __init__(self, lower_left_corner, width, height, num_arrows=10):
        box = Rectangle(lower_left_corner, width, height)
        self.shapes = {'box': box}
        dx = float(width)/(num_arrows-1)
        y_top = lower_left_corner[1] + height
        y_tip = lower_left_corner[1]
        for i in range(num_arrows):
            x = lower_left_corner[0] + i*dx
            self.shapes['arrow%d' % i] = Arrow1((x, y_top), (x, y_tip))

    def geometric_features(self):
        return {'mid_top': self.shapes['box'].geometric_features()['upper_mid']}


class Moment(Arc_wText):
    def __init__(self, text, center, radius,
                 left=True, counter_clockwise=True,
                 fontsize=0, text_spacing=1/60.):
        style = '->' if counter_clockwise else '<-'
        start_angle = 90 if left else -90
        Arc_wText.__init__(self, text, center, radius,
                           start_angle=start_angle,
                           arc_angle=180, fontsize=fontsize,
                           text_spacing=text_spacing,
                           resolution=180)
        self.shapes['arc'].set_arrow(style)


class Wheel(Shape):
    def __init__(self, center, radius, inner_radius=None, nlines=10):
        if inner_radius is None:
            inner_radius = radius/5.0

        outer = Circle(center, radius)
        inner = Circle(center, inner_radius)
        lines = []
        # Draw nlines+1 since the first and last coincide
        # (then nlines lines will be visible)
        t = linspace(0, 2*pi, self.nlines+1)

        Ri = inner_radius;  Ro = radius
        x0 = center[0];  y0 = center[1]
        xinner = x0 + Ri*cos(t)
        yinner = y0 + Ri*sin(t)
        xouter = x0 + Ro*cos(t)
        youter = y0 + Ro*sin(t)
        lines = [Line((xi,yi),(xo,yo)) for xi, yi, xo, yo in \
                 zip(xinner, yinner, xouter, youter)]
        self.shapes = {'inner': inner, 'outer': outer,
                       'spokes': Composition(
                           {'spoke%d' % i: lines[i]
                            for i in range(len(lines))})}

class SineWave(Shape):
    def __init__(self, xstart, xstop,
                 wavelength, amplitude, mean_level):
        self.xstart = xstart
        self.xstop = xstop
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.mean_level = mean_level

        npoints = (self.xstop - self.xstart)/(self.wavelength/61.0)
        x = linspace(self.xstart, self.xstop, npoints)
        k = 2*pi/self.wavelength # frequency
        y = self.mean_level + self.amplitude*sin(k*x)
        self.shapes = {'waves': Curve(x,y)}




class Spring(Shape):
    """
    Specify a *vertical* spring, starting at `start` and with `length`
    as total vertical length. In the middle of the spring there are
    `num_windings` circular windings to illustrate the spring. If
    `teeth` is true, the spring windings look like saw teeth,
    otherwise the windings are smooth circles.  The parameters `width`
    (total width of spring) and `bar_length` (length of first and last
    bar are given sensible default values if they are not specified
    (these parameters can later be extracted as attributes, see table
    below).
    """
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, width=None, bar_length=None,
                 num_windings=11, teeth=False):
        B = start
        n = num_windings - 1  # n counts teeth intervals
        if n <= 6:
            n = 7
        # n must be odd:
        if n % 2 == 0:
            n = n+1
        L = length
        if width is None:
            w = L/10.
        else:
            w = width/2.0
        s = bar_length

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.

        # B: start point
        # w: half-width
        # L: total length
        # s: length of first bar
        # P0: start of dashpot (B[0]+s)
        # P1: end of dashpot
        # P2: end point

        shapes = {}
        if s is None:
            f = Spring.spring_fraction
            s = L*(1-f)/2. # start of spring

        self.bar_length = s  # record
        self.width = 2*w

        P0 = (B[0], B[1] + s)
        P1 = (B[0], B[1] + L-s)
        P2 = (B[0], B[1] + L)

        if s >= L:
            raise ValueError('length of first bar: %g is larger than total length: %g' % (s, L))

        shapes['bar1'] = Line(B, P0)
        spring_length = L - 2*s
        t = spring_length/n  # height increment per winding
        if teeth:
            resolution = 4
        else:
            resolution = 90
        q = linspace(0, n, n*resolution + 1)
        x = P0[0] + w*sin(2*pi*q)
        y = P0[1] + q*t
        shapes['sprial'] = Curve(x, y)
        shapes['bar2'] = Line(P1,P2)
        self.shapes = shapes

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'width')
        length = Distance_wText((B[0]+3*w, B[1]), (B[0]+3*w, B[1]+L),
                                'length')
        num_windings = Text_wArrow('num_windings',
                                   (B[0]+2*w,P2[1]+w),
                                   (B[0]+1.2*w, B[1]+L/2.))
        blength1 = Distance_wText((B[0]-2*w, B[1]), (B[0]-2*w, P0[1]),
                                       'bar_length',
                                       text_pos=(P0[0]-7*w, P0[1]+w))
        blength2 = Distance_wText((P1[0]-2*w, P1[1]), (P2[0]-2*w, P2[1]),
                                       'bar_length',
                                       text_pos=(P2[0]-7*w, P2[1]+w))
        dims = {'start': start, 'width': width, 'length': length,
                'num_windings': num_windings, 'bar_length1': blength1,
                'bar_length2': blength2}
        self.dimensions = dims

    def geometric_features(self):
        """
        Recorded geometric features:

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        start                Start point of spring.
        end                  End point of spring.
        width                Total width of spring.
        bar_length           Length of first (and last) bar part.
        ==================== =============================================
        """
        b1 = self.shapes['bar1']
        d = {'start': b1.geometric_features()['start'],
             'end': self.shapes['bar2'].geometric_features()['end'],
             'bar_length': self.bar_length,
             'width': self.width}
        return d


class Dashpot(Shape):
    """
    Specify a vertical dashpot of height `total_length` and `start` as
    bottom/starting point. The first bar part has length `bar_length`.
    Then comes the dashpot as a rectangular construction of total
    width `width` and height `dashpot_length`. The position of the
    piston inside the rectangular dashpot area is given by
    `piston_pos`, which is the distance between the first bar (given
    by `bar_length`) to the piston.

    If some of `dashpot_length`, `bar_length`, `width` or `piston_pos`
    are not given, suitable default values are calculated. Their
    values can be extracted as keys in the dict returned from
    ``geometric_features``.

    """
    dashpot_fraction = 1./2            # fraction of total_length
    piston_gap_fraction = 1./6         # fraction of width
    piston_thickness_fraction = 1./8   # fraction of dashplot_length

    def __init__(self, start, total_length, bar_length=None,
                 width=None, dashpot_length=None, piston_pos=None):
        B = start
        L = total_length
        if width is None:
            w = L/10.    # total width 1/5 of length
        else:
            w = width/2.0
        s = bar_length

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.

        # B: start point
        # w: half-width
        # L: total length
        # s: length of first bar
        # P0: start of dashpot (B[0]+s)
        # P1: end of dashpot
        # P2: end point

        shapes = {}
        # dashpot is P0-P1 in y and width 2*w
        if dashpot_length is None:
            if s is None:
                f = Dashpot.dashpot_fraction
                s = L*(1-f)/2. # default
            P1 = (B[0], B[1]+L-s)
            dashpot_length = f*L
        else:
            if s is None:
                f = 1./2  # the bar lengths are taken as f*dashpot_length
                s = f*dashpot_length # default
            P1 = (B[0], B[1]+s+dashpot_length)
        P0 = (B[0], B[1]+s)
        P2 = (B[0], B[1]+L)

        if P2[1] > P1[1] > P0[1]:
            pass # ok
        else:
            raise ValueError('Dashpot has inconsistent dimensions! start: %g, dashpot begin: %g, dashpot end: %g, very end: %g' % (B[1], P0[1], P1[1], P2[1]))

        shapes['line start'] = Line(B, P0)

        shapes['pot'] = Curve([P1[0]-w, P0[0]-w, P0[0]+w, P1[0]+w],
                              [P1[1], P0[1], P0[1], P1[1]])
        piston_thickness = dashpot_length*Dashpot.piston_thickness_fraction
        if piston_pos is None:
            piston_pos = 1/3.*dashpot_length
        if piston_pos < 0:
            piston_pos = 0
        elif piston_pos > dashpot_length:
            piston_pos = dashpot_length - piston_thickness

        abs_piston_pos = P0[1] + piston_pos

        gap = w*Dashpot.piston_gap_fraction
        shapes['piston'] = Composition(
            {'line': Line(P2, (B[0], abs_piston_pos + piston_thickness)),
             'rectangle': Rectangle((B[0] - w+gap, abs_piston_pos),
                                    2*w-2*gap, piston_thickness),
             })
        shapes['piston']['rectangle'].set_filled_curves(pattern='X')

        self.shapes = shapes

        self.bar_length = s
        self.width = 2*w
        self.piston_pos = piston_pos
        self.dashpot_length = dashpot_length

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'width')
        dplength = Distance_wText((B[0]+2*w, P0[1]), (B[0]+2*w, P1[1]),
                                  'dashpot_length', text_pos=(B[0]+w,B[1]-w))
        blength = Distance_wText((B[0]-2*w, B[1]), (B[0]-2*w, P0[1]),
                                 'bar_length', text_pos=(B[0]-6*w,P0[1]-w))
        ppos    = Distance_wText((B[0]-2*w, P0[1]), (B[0]-2*w, P0[1]+piston_pos),
                                 'piston_pos', text_pos=(B[0]-6*w,P0[1]+piston_pos-w))
        tlength = Distance_wText((B[0]+4*w, B[1]), (B[0]+4*w, B[1]+L),
                                 'total_length',
                                 text_pos=(B[0]+4.5*w, B[1]+L-2*w))
        line = Line((B[0]+w, abs_piston_pos), (B[0]+7*w, abs_piston_pos)).set_linestyle('dashed').set_linecolor('black').set_linewidth(1)
        pp = Text('abs_piston_pos', (B[0]+7*w, abs_piston_pos), alignment='left')
        dims = {'start': start, 'width': width, 'dashpot_length': dplength,
                'bar_length': blength, 'total_length': tlength,
                'piston_pos': ppos,}
        #'abs_piston_pos': Composition({'line': line, 'text': pp})}
        self.dimensions = dims

    def geometric_features(self):
        """
        Recorded geometric features:

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        start                Start point of dashpot.
        end                  End point of dashpot.
        bar_length           Length of first bar (from start to spring).
        dashpot_length       Length of dashpot middle part.
        width                Total width of dashpot.
        piston_pos           Position of piston in dashpot, relative to
                             start[1] + bar_length.
        ==================== =============================================
        """
        d = {'start': self.shapes['line start'].geometric_features()['start'],
             'end': self.shapes['piston']['line'].geometric_features()['start'],
             'bar_length': self.bar_length,
             'piston_pos': self.piston_pos,
             'width': self.width,
             'dashpot_length': self.dashpot_length,
             }
        return d

class Wavy(Shape):
    def __init__(self, main_curve, interval, wavelength_of_perturbations,
                 amplitude_of_perturbations, smoothness):
        """
        ============================ ====================================
        Name                         Description
        ============================ ====================================
        main_curve                   f(x) Python function
        interval                     interval for main_curve
        wavelength_of_perturbations  dominant wavelength perturbed waves
        amplitude_of_perturbations   amplitude of perturbed waves
        smoothness                   in [0, 1]: smooth=0, rough=1
        ============================ ====================================
        """
        xmin, xmax = interval
        L = wavelength_of_perturbations
        k_0 = 2*pi/L    # main frequency of waves
        k_p = k_0*0.5
        k_k = k_0/2*smoothness

        A_0 = amplitude_of_perturbations
        A_p = 0.3*A_0
        A_k = k_0/2

        x = linspace(xmin, xmax, 2001)

        def w(x):
            A = A_0 + A_p*sin(A_k*x)
            k = k_0 + k_p*sin(k_k*x)
            y = main_curve(x) + A*sin(k*x)
            return y

        self.shapes = {'wavy': Curve(x, w(x))}
        # Use closure w to define __call__ - then we do not need
        # to store all the parameters A_0, A_k, etc. as attributes
        self.__call__ = w

# COMPOSITE types:
# MassSpringForce: Line(horizontal), Spring, Rectangle, Arrow/Line(w/arrow)
# must be easy to find the tip of the arrow
# Maybe extra dict: self.name['mass'] = Rectangle object - YES!

def test_Axis():
    drawing_tool.set_coordinate_system(
        xmin=0, xmax=15, ymin=-7, ymax=8, axis=True,
        instruction_file='tmp_Axis.py')
    x_axis = Axis((7.5,2), 5, 'x', rotation_angle=0)
    y_axis = Axis((7.5,2), 5, 'y', rotation_angle=90)
    system = Composition({'x axis': x_axis, 'y axis': y_axis})
    system.draw()
    drawing_tool.display()
    system.set_linestyle('dashed')
    system.rotate(40, (7.5,2))
    system.draw()
    drawing_tool.display()

    system.set_linestyle('dotted')
    system.rotate(220, (7.5,2))
    system.draw()
    drawing_tool.display()

    drawing_tool.display('Axis')
    drawing_tool.savefig('tmp_Axis.png')
    print repr(system)

def test_Distance_wText():
    drawing_tool.set_coordinate_system(xmin=0, xmax=10,
                                       ymin=0, ymax=6,
                                       axis=True,
                                       instruction_file='tmp_Distance_wText.py')
    #drawing_tool.arrow_head_width = 0.1
    fontsize=14
    t = r'$ 2\pi R^2 $'
    dims2 = Composition({
        'a0': Distance_wText((4,5), (8, 5), t, fontsize),
        'a6': Distance_wText((4,5), (4, 4), t, fontsize),
        'a1': Distance_wText((0,2), (2, 4.5), t, fontsize),
        'a2': Distance_wText((0,2), (2, 0), t, fontsize),
        'a3': Distance_wText((2,4.5), (0, 5.5), t, fontsize),
        'a4': Distance_wText((8,4), (10, 3), t, fontsize,
                             text_spacing=-1./60),
        'a5': Distance_wText((8,2), (10, 1), t, fontsize,
                             text_spacing=-1./40, alignment='right'),
        'c1': Text_wArrow('text_spacing=-1./60',
                          (4, 3.5), (9, 3.2),
                          fontsize=10, alignment='left'),
        'c2': Text_wArrow('text_spacing=-1./40, alignment="right"',
                          (4, 0.5), (9, 1.2),
                          fontsize=10, alignment='left'),
        })
    dims2.draw()
    drawing_tool.display('Distance_wText and text positioning')
    drawing_tool.savefig('tmp_Distance_wText.png')

def test_Rectangle():
    L = 3.0
    W = 4.0

    drawing_tool.set_coordinate_system(xmin=0, xmax=2*W,
                                       ymin=-L/2, ymax=2*L,
                                       axis=True,
                                       instruction_file='tmp_Rectangle.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = W/2
    r = Rectangle(lower_left_corner=(xpos,0), width=W, height=L)
    r.draw()
    r.draw_dimensions()
    drawing_tool.display('Rectangle')
    drawing_tool.savefig('tmp_Rectangle.png')


def test_Triangle():
    L = 3.0
    W = 4.0

    drawing_tool.set_coordinate_system(xmin=0, xmax=2*W,
                                       ymin=-L/2, ymax=1.2*L,
                                       axis=True,
                                       instruction_file='tmp_Triangle.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = 1
    t = Triangle(p1=(W/2,0), p2=(3*W/2,W/2), p3=(4*W/5.,L))
    t.draw()
    t.draw_dimensions()
    drawing_tool.display('Triangle')
    drawing_tool.savefig('tmp_Triangle.png')

def test_Arc():
    L = 4.0
    W = 4.0

    drawing_tool.set_coordinate_system(xmin=-W/2, xmax=W,
                                       ymin=-L/2, ymax=1.5*L,
                                       axis=True,
                                       instruction_file='tmp_Arc.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    center = point(0,0)
    radius = L/2
    start_angle = 60
    arc_angle = 45
    a = Arc(center, radius, start_angle, arc_angle)
    a.set_arrow('->')
    a.draw()

    R1 = 1.25*radius
    R2 = 1.5*radius
    R = 2*radius
    a.dimensions = {
        'start_angle': Arc_wText(
            'start_angle', center, R1, start_angle=0,
            arc_angle=start_angle, text_spacing=1/10.),
        'arc_angle': Arc_wText(
            'arc_angle', center, R2, start_angle=start_angle,
            arc_angle=arc_angle, text_spacing=1/20.),
        'r=0': Line(center, center +
                    point(R*cos(radians(start_angle)),
                          R*sin(radians(start_angle)))),
        'r=start_angle': Line(center, center +
                              point(R*cos(radians(start_angle+arc_angle)),
                                    R*sin(radians(start_angle+arc_angle)))),
        'r=start+arc_angle':  Line(center, center +
                                   point(R, 0)).set_linestyle('dashed'),
        'radius': Distance_wText(center, a(0), 'radius', text_spacing=1/40.),
        'center': Text('center', center-point(radius/10., radius/10.)),
        }
    for dimension in a.dimensions:
        dim = a.dimensions[dimension]
        dim.set_linestyle('dashed')
        dim.set_linewidth(1)
        dim.set_linecolor('black')

    a.draw_dimensions()
    drawing_tool.display('Arc')
    drawing_tool.savefig('tmp_Arc.png')


def test_Spring():
    L = 5.0
    W = 2.0

    drawing_tool.set_coordinate_system(xmin=0, xmax=7*W,
                                       ymin=-L/2, ymax=1.5*L,
                                       axis=True,
                                       instruction_file='tmp_Spring.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = W
    s1 = Spring((W,0), L, teeth=True)
    s1_title = Text('Default Spring', s1.geometric_features()['end'] + point(0,L/10))
    s1.draw()
    s1_title.draw()
    #s1.draw_dimensions()
    xpos += 3*W
    s2 = Spring(start=(xpos,0), length=L, width=W/2.,
                bar_length=L/6., teeth=False)
    s2.draw()
    s2.draw_dimensions()
    drawing_tool.display('Spring')
    drawing_tool.savefig('tmp_Spring.png')


def test_Dashpot():
    L = 5.0
    W = 2.0
    xpos = 0

    drawing_tool.set_coordinate_system(xmin=xpos, xmax=xpos+5.5*W,
                                       ymin=-L/2, ymax=1.5*L,
                                       axis=True,
                                       instruction_file='tmp_Dashpot.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    # Default (simple) dashpot
    xpos = 1.5
    d1 = Dashpot(start=(xpos,0), total_length=L)
    d1_title = Text('Dashpot (default)', d1.geometric_features()['end'] + point(0,L/10))
    d1.draw()
    d1_title.draw()

    # Dashpot for animation with fixed bar_length, dashpot_length and
    # prescribed piston_pos
    xpos += 2.5*W
    d2 = Dashpot(start=(xpos,0), total_length=1.2*L, width=W/2,
                 bar_length=W, dashpot_length=L/2, piston_pos=2*W)
    d2.draw()
    d2.draw_dimensions()

    drawing_tool.display('Dashpot')
    drawing_tool.savefig('tmp_Dashpot.png')

def test_Wavy():
    drawing_tool.set_coordinate_system(xmin=0, xmax=1.5,
                                       ymin=-0.5, ymax=5,
                                       axis=True,
                                       instruction_file='tmp_Wavy.py')
    w = Wavy(main_curve=lambda x: 1 + sin(2*x),
             interval=[0,1.5],
             wavelength_of_perturbations=0.3,
             amplitude_of_perturbations=0.1,
             smoothness=0.05)
    w.draw()
    drawing_tool.display('Wavy')
    drawing_tool.savefig('tmp_Wavy.png')

def diff_files(files1, files2, mode='HTML'):
    import difflib, time
    n = 3
    for fromfile, tofile in zip(files1, files2):
        fromdate = time.ctime(os.stat(fromfile).st_mtime)
        todate = time.ctime(os.stat(tofile).st_mtime)
        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()
        diff_html = difflib.HtmlDiff().\
                    make_file(fromlines,tolines,
                              fromfile,tofile,context=True,numlines=n)
        diff_plain = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
        filename_plain = fromfile + '.diff.txt'
        filename_html = fromfile + '.diff.html'
        if os.path.isfile(filename_plain):
            os.remove(filename_plain)
        if os.path.isfile(filename_html):
            os.remove(filename_html)
        f = open(filename_plain, 'w')
        f.writelines(diff_plain)
        f.close()
        size = os.path.getsize(filename_plain)
        if size > 4:
            print 'found differences:', fromfile, tofile
            f = open(filename_html, 'w')
            f.writelines(diff_html)
            f.close()


def test_test():
    os.chdir('test')
    funcs = [name for name in globals() if name.startswith('test_') and callable(globals()[name])]
    funcs.remove('test_test')
    new_files = []
    res_files = []
    for func in funcs:
        mplfile = func.replace('test_', 'tmp_') + '.py'
        #exec(func + '()')
        new_files.append(mplfile)
        resfile = mplfile.replace('tmp_', 'res_')
        res_files.append(resfile)
    diff_files(new_files, res_files)


def _test1():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line((0,0), (1,1))
    l1.draw()
    input(': ')
    c1 = Circle((5,2), 1)
    c2 = Circle((6,2), 1)
    w1 = Wheel((7,2), 1)
    c1.draw()
    c2.draw()
    w1.draw()
    hardcopy()
    display()  # show the plot

def _test2():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line((0,0), (1,1))
    l1.draw()
    input(': ')
    c1 = Circle((5,2), 1)
    c2 = Circle((6,2), 1)
    w1 = Wheel((7,2), 1)
    filled_curves(True)
    set_linecolor('blue')
    c1.draw()
    set_linecolor('aqua')
    c2.draw()
    filled_curves(False)
    set_linecolor('red')
    w1.draw()
    hardcopy()
    display()  # show the plot

def _test3():
    """Test example from the book."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line(start=(0,0), stop=(1,1))  # define line
    l1.draw()        # make plot data
    r1 = Rectangle(lower_left_corner=(0,1), width=3, height=5)
    r1.draw()
    Circle(center=(5,7), radius=1).draw()
    Wheel(center=(6,2), radius=2, inner_radius=0.5, nlines=7).draw()
    hardcopy()
    display()

def _test4():
    """Second example from the book."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    r1 = Rectangle(lower_left_corner=(0,1), width=3, height=5)
    c1 = Circle(center=(5,7), radius=1)
    w1 = Wheel(center=(6,2), radius=2, inner_radius=0.5, nlines=7)
    c2 = Circle(center=(7,7), radius=1)
    filled_curves(True)
    c1.draw()
    set_linecolor('blue')
    r1.draw()
    set_linecolor('aqua')
    c2.draw()
    # Add thick aqua line around rectangle:
    filled_curves(False)
    set_linewidth(4)
    r1.draw()
    set_linecolor('red')
    # Draw wheel with thick lines:
    w1.draw()
    hardcopy('tmp_colors')
    display()


def _test5():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    c = 6.  # center point of box
    w = 2.  # size of box
    L = 3
    r1 = Rectangle((c-w/2, c-w/2), w, w)
    l1 = Line((c,c-w/2), (c,c-w/2-L))
    linecolor('blue')
    filled_curves(True)
    r1.draw()
    linecolor('aqua')
    filled_curves(False)
    l1.draw()
    hardcopy()
    display()  # show the plot

def rolling_wheel(total_rotation_angle):
    """Animation of a rotating wheel."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)

    import time
    center = (6,2)
    radius = 2.0
    angle = 2.0
    pngfiles = []
    w1 = Wheel(center=center, radius=radius, inner_radius=0.5, nlines=7)
    for i in range(int(total_rotation_angle/angle)):
        w1.draw()
        print 'XXXX BIG PROBLEM WITH ANIMATE!!!'
        display()


        filename = 'tmp_%03d' % i
        pngfiles.append(filename + '.png')
        hardcopy(filename)
        time.sleep(0.3)  # pause

        L = radius*angle*pi/180  # translation = arc length
        w1.rotate(angle, center)
        w1.translate((-L, 0))
        center = (center[0] - L, center[1])

        erase()
    cmd = 'convert -delay 50 -loop 1000 %s tmp_movie.gif' \
          % (' '.join(pngfiles))
    print 'converting PNG files to animated GIF:\n', cmd
    import commands
    failure, output = commands.getstatusoutput(cmd)
    if failure:  print 'Could not run', cmd


if __name__ == '__main__':
    #rolling_wheel(40)
    #_test1()
    #_test3()
    funcs = [
        #test_Axis,
        test_inclined_plane,
        ]
    for func in funcs:
        func()
        raw_input('Type Return: ')


