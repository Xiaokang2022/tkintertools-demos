import typing

import matplotlib.animation as animation
import matplotlib.figure as figure
import matplotlib.pyplot as pyplot
import numpy
import tkintertools as tkt
import tkintertools.animation.animations as animations
import tkintertools.animation.controllers as controllers
import tkintertools.core.constants as constants
import tkintertools.mpl as mpl
import tkintertools.style as style
import tkintertools.toolbox as toolbox

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    constants.FONT = "LXGW WenKai"

mpl.set_mpl_default_theme(style.get_color_mode(), apply_font=True)

"""
1st Window
"""

# fig = figure.Figure()
# ax = fig.add_subplot(projection='3d')

# colors = ['r', 'g', 'b', 'y']
# yticks = [3, 2, 1, 0]

# for c, k in zip(colors, yticks):
#     xs = numpy.arange(20)
#     ys = numpy.random.rand(20)
#     cs = [c] * len(xs)
#     cs[0] = 'c'
#     ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title("3D")

# ax.set_yticks(yticks)

# root = tkt.Tk((960, 720), title="Matplotlib Test - 3D Plot")
# root.center()
# canvas = tkt.Canvas(root, zoom_item=True)
# canvas.place(width=960, height=720)
# figure_canvas = mpl.FigureCanvas(canvas, fig)
# toolbar = mpl.FigureToolbar(canvas, figure_canvas)
# figure_canvas.pack(side="top", fill="both", expand=True)

# root.mainloop()

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
figure_canvas = mpl.FigureCanvas(canvas, fig)
toolbar = mpl.FigureToolbar(canvas, figure_canvas)
figure_canvas.pack(side="top", fill="both", expand=True)


root.mainloop()

"""
3st Window
"""

# NOTE: This example is experimental!
# TIPS: You can choose two different backends for the animation below

# ANIMATION_BACKEND: typing.Literal["mpl", "tkt"] = "mpl"

# fig = figure.Figure() if ANIMATION_BACKEND == "tkt" else pyplot.figure()
# ax = fig.add_subplot()
# ax.grid()
# ax.set(xlabel='x', ylabel='y', title='Animated line plot')

# x = numpy.arange(0, 2*numpy.pi, 0.01)
# line, = ax.plot(x, numpy.sin(x))


# def animate(i):
#     line.set_ydata(numpy.sin(x + i / 50))  # update the data.
#     return line,


# ani = animation.FuncAnimation(
#     fig, animate, interval=1, blit=True, save_count=50)

# root = tkt.Tk((960, 720), title="Matplotlib Test - Normal Plot")
# root.center()
# canvas = tkt.Canvas(root, zoom_item=True)
# canvas.place(width=960, height=720)
# figure_canvas = mpl.FigureCanvas(canvas, fig)
# toolbar = mpl.FigureToolbar(canvas, figure_canvas)
# figure_canvas.pack(side="top", fill="both", expand=True)


# if ANIMATION_BACKEND == "tkt":
#     animations.Animation(1000, callback=lambda _: ani._step(),
#                         controller=controllers.flat, repeat=-1).start()
# else:
#     root.shutdown(pyplot.close, ensure_destroy=True)


# root.mainloop()
