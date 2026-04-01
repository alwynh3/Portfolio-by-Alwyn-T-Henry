import schemdraw
import schemdraw.dsp as dsp

d = schemdraw.Drawing()
d.config(fontsize=12, font='sans-serif', lw=1.5)

# Equation 1: x_ddot = f(t) - 2x_dot + 2y_dot - x
# Equation 2: y_dot = 5g(t) + x - y

# Left summing junction for X
d += dsp.Line().length(1.5).label('f(t)', 'left')
sum_x = d += dsp.Mixer(label='', plabels={'+': 'L', '-': 'B', '+': 'T'}).label('Σ', 'right')

# First X Integrator
d += dsp.Line().right().length(1.5).label('x_ddot', 'top')
int_x1 = d += dsp.Box(w=1.2, h=1.2).label('$\\int$')
d += dsp.Line().right().length(1.5).label('x_dot', 'top')

# Second X Integrator
int_x2 = d += dsp.Box(w=1.2, h=1.2).label('$\\int$')
d += dsp.Line().right().length(2).label('x', 'top')

d.save('diagram_style_test.png')
print("Saved")
