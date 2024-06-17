import matplotlib.figure as figure
import numpy
import tkintertools as tkt
import tkintertools.style as style
import tkintertools.toolbox.mpl as mpl

mpl.set_mpl_default_theme(style.get_color_mode() == "dark")

"""
1st Window
"""

fig = figure.Figure()
ax = fig.add_subplot(projection='3d')

colors = ['r', 'g', 'b', 'y']
yticks = [3, 2, 1, 0]

for c, k in zip(colors, yticks):
    xs = numpy.arange(20)
    ys = numpy.random.rand(20)
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("3D")

ax.set_yticks(yticks)

root = tkt.Tk((960, 720), title="Matplotlib Test - 3D Plot")
root.center()
canvas = tkt.Canvas(root, zoom_item=True)
canvas.place(width=960, height=720)
figure_canvas = mpl.FigureCanvas(fig, canvas)
toolbar = mpl.FigureToolbar(figure_canvas, canvas)
figure_canvas.pack(side="top", fill="both", expand=True)

root.mainloop()

"""
2nd Winodow
"""

t = numpy.arange(0.0, 2.0, 0.01)
s = 1 + numpy.sin(2 * numpy.pi * t)

fig = figure.Figure()
ax = fig.add_subplot()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()
ax.legend(["y=sin(x)"])

root = tkt.Tk((960, 720), title="Matplotlib Test - Normal Plot")
root.center()
canvas = tkt.Canvas(root, zoom_item=True)
canvas.place(width=960, height=720)
figure_canvas = mpl.FigureCanvas(fig, canvas)
toolbar = mpl.FigureToolbar(figure_canvas, canvas)
figure_canvas.pack(side="top", fill="both", expand=True)


root.mainloop()
