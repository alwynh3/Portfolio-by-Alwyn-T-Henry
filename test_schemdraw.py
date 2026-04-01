import schemdraw
import schemdraw.dsp as dsp

d = schemdraw.Drawing()
d += dsp.Line().length(2).label('x', 'left')
sum1 = d += dsp.Mixer(label='Σ')
d += dsp.Arrow().right().length(2)
int1 = d += dsp.Box(h=1.2, w=1.2).label('∫')
d += dsp.Arrow().right().length(2)
sum2 = d += dsp.Mixer(label='Σ')
d += dsp.Arrow().right().length(2).label('z', 'right')

# feedback
d += dsp.Line().down().at(sum1.S).length(2)
d += dsp.Line().right().tox(int1.S)
d += dsp.Arrow().up().toy(int1.S)

d.save('diagram_b1_test.png')
print("Diagram generated")
