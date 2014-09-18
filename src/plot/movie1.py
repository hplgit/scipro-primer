from scitools.std import sqrt, pi, exp, linspace, plot, movie
import time, glob, os, sys

# Clean up old frames
for name in glob.glob('tmp_*.pdf'):
    os.remove(name)

def f(x, m, s):
    return (1.0/(sqrt(2*pi)*s))*exp(-0.5*((x-m)/s)**2)

m = 0
s_max = 2
s_min = 0.2
x = linspace(m -3*s_max, m + 3*s_max, 1000)
s_values = linspace(s_max, s_min, 30)
# f is max for x=m; smaller s gives larger max value
max_f = f(m, m, s_min)

# Show the movie, and make hardcopies of frames simulatenously
counter = 0
for s in s_values:
    y = f(x, m, s)
    plot(x, y, '-', axis=[x[0], x[-1], -0.1, max_f],
         xlabel='x', ylabel='f', legend='s=%4.2f' % s,
         savefig='tmp_%04d.png' % counter)
    counter += 1
    #time.sleep(0.2)  # can insert a pause to control movie speed

if '--no-moviefile' in sys.argv:
    # Drop making movie files
    import sys; sys.exit(0)

# Animated GIF
cmd = 'convert -delay 50 tmp_*.png movie1.gif'
os.system(cmd)

# Flash video
basic = 'avconv -r 12 -i tmp_%04d.png -c:v '
cmd = basic + 'flv movie1.flv'
os.system(cmd)

# MP4 video
cmd = basic + 'libx264 movie1.mp4'
os.system(cmd)

# Ogg video
cmd = basic + 'libtheora movie1.ogg'
os.system(cmd)

# WebM video
cmd = basic + 'libvpx movie1.webm'
os.system(cmd)

# HTML (via scitools.easyviz.movie)
movie('tmp_*.png', encoder='html', fps=3,
      output_file='tmpmovie.html')  # play in HTML file

