import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms
import numpy as np

class MatplotlibDraw:
    """
    Simple interface for plotting. This interface makes use of
    Matplotlib for plotting.

    Some attributes that must be controlled directly (no set_* method
    since these attributes are changed quite seldom).

    ========================== ============================================
    Attribute                  Description
    ========================== ============================================
    allow_screen_graphics      False means that no plot is shown on
                               the screen. (Does not work yet.)
    arrow_head_width           Size of arrow head.
    ========================== ============================================
    """

    line_colors = {'red': 'r', 'green': 'g', 'blue': 'b', 'cyan': 'c',
                   'magenta': 'm', 'purple': 'p',
                   'yellow': 'y', 'black': 'k', 'white': 'w',
                   'brown': 'brown', '': ''}
    def __init__(self):
        self.instruction_file = None
        self.allow_screen_graphics = True  # does not work yet

    def __del__(self):
        if self.instruction_file:
            self.instruction_file.write('\nmpl.draw()\nraw_input()\n')
            self.instruction_file.close()

    def ok(self):
        """
        Return True if set_coordinate_system is called and
        objects can be drawn.
        """

    def adjust_coordinate_system(self, minmax, occupation_percent=80):
        """
        Given a dict of xmin, xmax, ymin, ymax values, and a desired
        filling of the plotting area of `occupation_percent` percent,
        set new axis limits.
        """
        x_range = minmax['xmax'] - minmax['xmin']
        y_range = minmax['ymax'] - minmax['ymin']
        new_x_range = x_range*100./occupation_percent
        x_space = new_x_range - x_range
        new_y_range = y_range*100./occupation_percent
        y_space = new_y_range - y_range
        self.ax.set_xlim(minmax['xmin']-x_space/2., minmax['xmax']+x_space/2.)
        self.ax.set_ylim(minmax['ymin']-y_space/2., minmax['ymax']+y_space/2.)

    def set_coordinate_system(self, xmin, xmax, ymin, ymax, axis=False,
                              instruction_file=None):
        """
        Define the drawing area [xmin,xmax]x[ymin,ymax].
        axis: None or False means that axes with tickmarks
        are not drawn.
        instruction_file: name of file where all the instructions
        for the plotting program are stored (useful for debugging
        a figure or tailoring plots).
        """

        # Close file for previous figure and start new one
        # if not the figure file is the same
        if self.instruction_file is not None:
            if instruction_file == self.instruction_file.name:
                pass  # continue with same file
            else:
                self.instruction_file.close()  # make new py file for commands

        self.mpl = mpl
        self.xmin, self.xmax, self.ymin, self.ymax = \
             float(xmin), float(xmax), float(ymin), float(ymax)
        self.xrange = self.xmax - self.xmin
        self.yrange = self.ymax - self.ymin
        self.axis = axis

        # Compute the right X11 geometry on the screen based on the
        # x-y ratio of axis ranges
        ratio = (self.ymax-self.ymin)/(self.xmax-self.xmin)
        self.xsize = 800  # pixel size
        self.ysize = self.xsize*ratio
        geometry = '%dx%d' % (self.xsize, self.ysize)
        # See http://stackoverflow.com/questions/7449585/how-do-you-set-the-absolute-position-of-figure-windows-with-matplotlib

        if isinstance(instruction_file, str):
            self.instruction_file = open(instruction_file, 'w')
        else:
            self.instruction_file = None

        self.mpl.ion()  # important for interactive drawing and animation
        if self.instruction_file:
            self.instruction_file.write("""\
import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms

mpl.ion()  # for interactive drawing
""")
        # Default properties
        self.set_linecolor('red')
        self.set_linewidth(2)
        self.set_linestyle('solid')
        self.set_filled_curves()  # no filling
        self.set_fontsize(14)
        self.arrow_head_width = 0.2*self.xrange/16

        self._make_axes(new_figure=True)

        manager = self.mpl.get_current_fig_manager()
        manager.window.wm_geometry(geometry)

    def _make_axes(self, new_figure=False):
        if new_figure:
            self.fig = self.mpl.figure()
        self.ax = self.fig.gca()
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_aspect('equal')  # extent of 1 unit is the same on the axes

        if not self.axis:
            self.mpl.axis('off')
            axis_cmd = "mpl.axis('off')  # do not show axes with tickmarks\n"
        else:
            axis_cmd = ''

        if self.instruction_file:
            fig = 'fig = mpl.figure()\n' if new_figure else ''
            self.instruction_file.write("""\
%s
ax = fig.gca()
xmin, xmax, ymin, ymax = %s, %s, %s, %s
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')
%s

""" % (fig, self.xmin, self.xmax, self.ymin, self.ymax, axis_cmd))

    def inside(self, pt, exception=False):
        """Is point pt inside the defined plotting area?"""
        area = '[%s,%s]x[%s,%s]' % \
               (self.xmin, self.xmax, self.ymin, self.ymax)
        tol = 1E-14
        pt_inside = True
        if self.xmin - tol <= pt[0] <= self.xmax + tol:
            pass
        else:
            pt_inside = False
        if self.ymin - tol <= pt[1] <= self.ymax + tol:
            pass
        else:
            pt_inside = False
        if pt_inside:
            return pt_inside, 'point=%s is inside plotting area %s' % \
                   (pt, area)
        else:
            msg = 'point=%s is outside plotting area %s' % (pt, area)
            if exception:
                raise ValueError(msg)
            return pt_inside, msg

    def set_linecolor(self, color):
        """
        Change the color of lines. Available colors are
        'black', 'white', 'red', 'blue', 'green', 'yellow',
        'magenta', 'cyan'.
        """
        self.linecolor = MatplotlibDraw.line_colors[color]

    def set_linestyle(self, style):
        """Change line style: 'solid', 'dashed', 'dashdot', 'dotted'."""
        if not style in ('solid', 'dashed', 'dashdot', 'dotted'):
            raise ValueError('Illegal line style: %s' % style)
        self.linestyle = style

    def set_linewidth(self, width):
        """Change the line width (int, starts at 1)."""
        self.linewidth = width

    def set_filled_curves(self, color='', pattern=''):
        """
        Fill area inside curves with specified color and/or pattern.
        A common pattern is '/' (45 degree lines). Other patterns
        include '-', '+', 'x', '\\', '*', 'o', 'O', '.'.
        """
        if color is False:
            self.fillcolor = ''
            self.fillpattern = ''
        else:
            self.fillcolor = color if len(color) == 1 else \
                         MatplotlibDraw.line_colors[color]
            self.fillpattern = pattern

    def set_fontsize(self, fontsize=18):
        """
        Method for setting a common fontsize for text, unless
        individually specified when calling ``text``.
        """
        self.fontsize = fontsize

    def set_grid(self, on=False):
        self.mpl.grid(on)
        if self.instruction_file:
            self.instruction_file.write("\nmpl.grid(%s)\n" % str(on))

    def erase(self):
        """Erase the current figure."""
        self.mpl.delaxes()
        if self.instruction_file:
            self.instruction_file.write("\nmpl.delaxes()  # erase\n")

        self._make_axes(new_figure=False)

    def plot_curve(self, x, y,
                   linestyle=None, linewidth=None,
                   linecolor=None, arrow=None,
                   fillcolor=None, fillpattern=None,
                   shadow=0, name=None):
        """Define a curve with coordinates x and y (arrays)."""
        #if not self.allow_screen_graphics:
        #    mpl.ioff()
        #else:
        #    mpl.ion()

        self.xdata = np.asarray(x, dtype=np.float)
        self.ydata = np.asarray(y, dtype=np.float)

        if linestyle is None:
            # use "global" linestyle
            linestyle = self.linestyle
        if linecolor is None:
            linecolor = self.linecolor
        if linewidth is None:
            linewidth = self.linewidth
        if fillcolor is None:
            fillcolor = self.fillcolor
        if fillpattern is None:
            fillpattern = self.fillpattern
        if shadow == 1:
            shadow = 3   # smallest displacement that is visible

        # We can plot fillcolor/fillpattern, arrow or line

        if self.instruction_file:
            import pprint
            if name is not None:
                self.instruction_file.write('\n# %s\n' % name)
            if not arrow:
                self.instruction_file.write(
                    'x = %s\n' % pprint.pformat(self.xdata.tolist()))
                self.instruction_file.write(
                    'y = %s\n' % pprint.pformat(self.ydata.tolist()))


        if fillcolor or fillpattern:
            if fillpattern != '':
                fillcolor = 'white'
            #print '%d coords, fillcolor="%s" linecolor="%s" fillpattern="%s"' % (x.size, fillcolor, linecolor, fillpattern)
            [line] = self.ax.fill(x, y, fillcolor, edgecolor=linecolor,
                                  linewidth=linewidth, hatch=fillpattern)
            if self.instruction_file:
                self.instruction_file.write("[line] = ax.fill(x, y, '%s', edgecolor='%s', linewidth=%d, hatch='%s')\n" % (fillcolor, linecolor, linewidth, fillpattern))

        elif arrow:
            # Note that a Matplotlib arrow is a line with the arrow tip
            # (do not draw the line in addition)
            if not arrow in ('->', '<-', '<->'):
                raise ValueError("arrow argument must be '->', '<-', or '<->', not %s" % repr(arrow))

            # Add arrow to first and/or last segment
            start = arrow == '<-' or arrow == '<->'
            end = arrow == '->' or arrow == '<->'
            if start:
                x_s, y_s = x[1], y[1]
                dx_s, dy_s = x[0]-x[1], y[0]-y[1]
                self._plot_arrow(x_s, y_s, dx_s, dy_s, '->',
                                 linestyle, linewidth, linecolor)
            if end:
                x_e, y_e = x[-2], y[-2]
                dx_e, dy_e = x[-1]-x[-2], y[-1]-y[-2]
                self._plot_arrow(x_e, y_e, dx_e, dy_e, '->',
                                 linestyle, linewidth, linecolor)
        else:
            # Plain line
            [line] = self.ax.plot(x, y, linecolor, linewidth=linewidth,
                                  linestyle=linestyle)
            if self.instruction_file:
                self.instruction_file.write("[line] = ax.plot(x, y, '%s', linewidth=%d, linestyle='%s')\n" % (linecolor, linewidth, linestyle))

        if shadow:
            # http://matplotlib.sourceforge.net/users/transforms_tutorial.html#using-offset-transforms-to-create-a-shadow-effect
            # shift the object over 2 points, and down 2 points
            dx, dy = shadow/72., -shadow/72.
            offset = transforms.ScaledTranslation(
                dx, dy, self.fig.dpi_scale_trans)
            shadow_transform = self.ax.transData + offset
            # now plot the same data with our offset transform;
            # use the zorder to make sure we are below the line
            if linewidth is None:
                linewidth = 3
            self.ax.plot(x, y, linewidth=linewidth, color='gray',
                         transform=shadow_transform,
                         zorder=0.5*line.get_zorder())


            if self.instruction_file:
                self.instruction_file.write("""
# Shadow effect for last ax.plot
dx, dy = 3/72., -3/72.
offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
shadow_transform = ax.transData + offset
self.ax.plot(x, y, linewidth=%d, color='gray',
             transform=shadow_transform,
             zorder=0.5*line.get_zorder())
""" % linewidth)



    def display(self, title=None):
        """Display the figure."""
        if title is not None:
            self.mpl.title(title)
            if self.instruction_file:
                self.instruction_file.write('mpl.title("%s")\n' % title)

        self.mpl.draw()

        if self.instruction_file:
            self.instruction_file.write('mpl.draw()\n')

    def savefig(self, filename, dpi=None):
        """Save figure in file. Set dpi=300 for really high resolution."""
        # If filename is without extension, generate all important formats
        ext = os.path.splitext(filename)[1]
        if not ext:
            self.mpl.savefig(filename + '.png', dpi=dpi)
            # Crop the PNG file
            failure = os.system('convert -trim %s.png %s.png' %
                                (filename, filename))
            if failure:
                print 'convert from ImageMagick is not installed - needed for cropping PNG files'
            self.mpl.savefig(filename + '.pdf')
            failure = os.system('pdfcrop %s.pdf %s.pdf' %
                                (filename, filename))
            if failure:
                print 'pdfcrop is not installed - needed for cropping PDF files'
            #self.mpl.savefig(filename + '.eps')
            if self.instruction_file:
                self.instruction_file.write('mpl.savefig("%s.png", dpi=%s)\n'
                                            % (filename, dpi))
                self.instruction_file.write('mpl.savefig("%s.pdf")\n'
                                            % filename)
        else:
            self.mpl.savefig(filename, dpi=dpi)
            if ext == '.png':
                failure = os.system('convert -trim %s %s' % (filename, filename))
                if failure:
                    print 'convert from ImageMagick is not installed - needed for cropping PNG files'
            elif ext == '.pdf':
                failure = os.system('pdfcrop %s %s' % (filename, filename))
                if failure:
                    print 'pdfcrop is not installed - needed for cropping PDF files'

            if self.instruction_file:
                self.instruction_file.write('mpl.savefig("%s", dpi=%s)\n'
                                            % (filename, dpi))


    def text(self, text, position, alignment='center', fontsize=0,
             arrow_tip=None):
        """
        Write `text` string at a position (centered, left, right - according
        to the `alignment` string). `position` is a point in the coordinate
        system.
        If ``arrow+tip != None``, an arrow is drawn from the text to a point
        (on a curve, for instance). The arrow_tip argument is then
        the (x,y) coordinates for the arrow tip.
        fontsize=0 indicates use of the default font as set by
        ``set_fontsize``.
        """
        if fontsize == 0:
            if hasattr(self, 'fontsize'):
                fontsize = self.fontsize
            else:
                raise AttributeError(
                    'No self.fontsize attribute to be used when text(...)\n'
                    'is called with fontsize=0. Call set_fontsize method.')

        x, y = position
        if arrow_tip is None:
            self.ax.text(x, y, text, horizontalalignment=alignment,
                         fontsize=fontsize)
            if self.instruction_file:
                self.instruction_file.write("""\
ax.text(%g, %g, %s,
        horizontalalignment=%s, fontsize=%d)
""" % (x, y, repr(text), repr(alignment), fontsize))
        else:
            if not len(arrow_tip) == 2:
                raise ValueError('arrow_tip=%s must be (x,y) pt.' % arrow)
            pt = arrow_tip
            self.ax.annotate(text, xy=pt, xycoords='data',
                             textcoords='data', xytext=position,
                             horizontalalignment=alignment,
                             verticalalignment='top',
                             fontsize=fontsize,
                             arrowprops=dict(arrowstyle='->',
                                             facecolor='black',
                                             #linewidth=2,
                                             linewidth=1,
                                             shrinkA=5,
                                             shrinkB=5))
            if self.instruction_file:
                self.instruction_file.write("""\
ax.annotate('%s', xy=%s, xycoords='data',
            textcoords='data', xytext=%s,
            horizontalalignment='%s',
            verticalalignment='top',
            fontsize=%d,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))
""" % (text, pt, position, alignment, fontsize))

# Drawing annotations with arrows:
#http://matplotlib.sourceforge.net/users/annotations_intro.html
#http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/annotation_demo2.py
#http://matplotlib.sourceforge.net/users/annotations_intro.html
#http://matplotlib.sourceforge.net/users/annotations_guide.html#plotting-guide-annotation

    def _plot_arrow(self, x, y, dx, dy, style='->',
                    linestyle=None, linewidth=None, linecolor=None):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        if linestyle is None:
            # use "global" linestyle
            linestyle = self.linestyle
        if linecolor is None:
            linecolor = self.linecolor
        if linewidth is None:
            linewidth = self.linewidth

        if style == '->' or style == '<->':
            self.mpl.arrow(x, y, dx, dy, hold=True,
                           facecolor=linecolor,
                           edgecolor=linecolor,
                           linestyle=linestyle,
                           linewidth=linewidth,
                           head_width=self.arrow_head_width,
                           #head_width=0.1,
                           #width=1,  # width of arrow body in coordinate scale
                           length_includes_head=True,
                           shape='full')
            if self.instruction_file:
                self.instruction_file.write("""\
mpl.arrow(x=%g, y=%g, dx=%g, dy=%g,
          facecolor='%s', edgecolor='%s',
          linestyle='%s',
          linewidth=%g, head_width=0.1,
          length_includes_head=True,
          shape='full')
""" % (x, y, dx, dy, linecolor, linecolor, linestyle, linewidth))
        if style == '<-' or style == '<->':
            self.mpl.arrow(x+dx, y+dy, -dx, -dy, hold=True,
                           facecolor=linecolor,
                           edgecolor=linecolor,
                           linewidth=linewidth,
                           head_width=0.1,
                           #width=1,
                           length_includes_head=True,
                           shape='full')
            if self.instruction_file:
                self.instruction_file.write("""\
mpl.arrow(x=%g, y=%g, dx=%g, dy=%g,
          facecolor='%s', edgecolor='%s',
          linewidth=%g, head_width=0.1,
          length_includes_head=True,
          shape='full')
""" % (x+dx, y+dy, -dx, -dy, linecolor, linecolor, linewidth))

    def arrow2(self, x, y, dx, dy, style='->'):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        self.ax.annotate('', xy=(x+dx,y+dy), xytext=(x,y),
                         arrowprops=dict(arrowstyle=style,
                                         facecolor='black',
                                         linewidth=1,
                                         shrinkA=0,
                                         shrinkB=0))
        if self.instruction_file:
            self.instruction_file.write("""
ax.annotate('', xy=(%s,%s), xytext=(%s,%s),
                         arrowprops=dict(arrowstyle=%s,
                                         facecolor='black',
                                         linewidth=1,
                                         shrinkA=0,
                                         shrinkB=0))
""" % (x+dx, y+dy, x, y, style))



def _test():
    d = MatplotlibDraw(0, 10, 0, 5, instruction_file='tmp3.py', axis=True)
    d.set_linecolor('magenta')
    d.set_linewidth(6)
    # triangle
    x = np.array([1, 4, 1, 1]);  y = np.array([1, 1, 4, 1])
    d.set_filled_curves('magenta')
    d.plot_curve(x, y)
    d.set_filled_curves(False)
    d.plot_curve(x+4, y)
    d.text('some text1', position=(8,4), arrow_tip=(6, 1), alignment='left',
           fontsize=18)
    pos = np.array((7,4.5))  # numpy points work fine
    d.text('some text2', position=pos, arrow_tip=(6, 1), alignment='center',
           fontsize=12)
    d.set_linewidth(2)
    d.arrow(0.25, 0.25, 0.45, 0.45)
    d.arrow(0.25, 0.25, 0.25, 4, style='<->')
    d.arrow2(4.5, 0, 0, 3, style='<->')
    x = np.linspace(0, 9, 201)
    y = 4.5 + 0.45*np.cos(0.5*np.pi*x)
    d.plot_curve(x, y, arrow='end')
    d.display()
    raw_input()

if __name__ == '__main__':
    _test()
