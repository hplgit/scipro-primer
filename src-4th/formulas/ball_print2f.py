v0 = 5
g = 9.81
t = 0.6
y = v0*t - 0.5*g*t**2

print """
At t={t:f} s, a ball with
initial velocity v0={v0:.3E} m/s
is located at the height {y:.2f} m.
""".format(t=t, v0=v0, y=y)

