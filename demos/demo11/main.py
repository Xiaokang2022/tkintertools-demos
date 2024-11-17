import itertools
import math
import statistics

import matplotlib.figure as figure
import numpy
import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.core.configs as configs
import tkintertools.media as media
import tkintertools.mpl as mpl
import tkintertools.style as style
import tkintertools.three as three
import tkintertools.toolbox as toolbox

# Optional operations #

# configs.Env.system = "Windows10"

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

mpl.set_mpl_default_theme(style.get_color_mode(), apply_font=True)

# Optional operations #


# tkintertools-mpl-1 #
t1 = numpy.arange(0.0, 2.0, 0.01)
s1 = 1 + numpy.sin(2 * numpy.pi * t1)

fig1 = figure.Figure()
ax1 = fig1.add_subplot()
ax1.plot(t1, s1)

ax1.set(
    xlabel="time (s)",
    ylabel="voltage (mV)",
    title="Plotting based on the theme in tkt",
)
ax1.grid()
ax1.legend(["y=sin(x)"])
# tkintertools-mpl #


# tkintertools-mpl-2 #
fig2 = figure.Figure()
ax2 = fig2.add_subplot(projection='3d')

colors = ['r', 'g', 'b', 'y']
yticks = [3, 2, 1, 0]

for c, k in zip(colors, yticks):
    xs = numpy.arange(20)
    ys = numpy.random.rand(20)
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax2.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title("3D plotting with interoperability")

ax2.set_yticks(yticks)
# tkintertools-mpl #


root = tkt.Tk((1920, 1080), title="Extension Test")

# Optional operations #
# style.customize_window(root, boarder_type="rectangular")
# Optional operations #

root.center()
cv = tkt.Canvas(root, keep_ratio="min", free_anchor=True, zoom_item=True)
cv.place(width=1920, height=1080, x=960, y=540, anchor="center")

cv_mpl_1 = mpl.FigureCanvas(cv, fig1)
toolbar_1 = mpl.FigureToolbar(cv_mpl_1)
cv_mpl_1.place(width=960, height=540)

cv_mpl_2 = mpl.FigureCanvas(cv, fig2)
toolbar_2 = mpl.FigureToolbar(cv_mpl_2)
cv_mpl_2.place(width=960, height=540, x=960, y=540)

# tkintertools-media #
cv_media = media.VideoCanvas(
    cv, keep_ratio="min", free_anchor=True, controls=True)
cv_media.place(width=960, height=540, x=960)
cv_media.open("./assets/videos/Bad Apple.mp4")
# tkintertools-media #


# tkintertools-3d #
space = three.Space(cv, free_anchor=True, zoom_item=True, highlightthickness=0,
                    keep_ratio="min", bg="black" if style.get_color_mode() == "dark" else "white")
space.place(width=960, height=540, y=540)
space.update()

style.register_event(lambda flag: space.configure(
    bg="black" if flag else "white"))

m = 150 * math.sqrt(50 - 10 * math.sqrt(5)) / 10
n = 150 * math.sqrt(50 + 10 * math.sqrt(5)) / 10
points = []
dis_side = 150 * (3 * math.sqrt(3) + math.sqrt(15)) / 12 / \
    ((math.sqrt(10 + 2 * math.sqrt(5))) / 4)
count, color_lst = 0, ['00', '77', 'FF']
colors = [f'#{r}{g}{b}' for r in color_lst for g in color_lst for b in color_lst]

for i in m, -m:
    for j in n, -n:
        points.append([0, j, i])
        points.append([i, 0, j])
        points.append([j, i, 0])

for p in itertools.combinations(points, 3):
    dis = math.hypot(*[statistics.mean(c[i] for c in p) for i in range(3)])
    if math.isclose(dis, dis_side):
        three.Plane(space, *p, fill=colors[count], outline='grey')
        count += 1


space.space_sort()


count = 0


def _callback(_: float) -> None:
    """callback function of animation"""
    global count
    count += 0.08
    for item in space.components:
        item.rotate(dy=-0.01, dz=0.02)
        item.translate(dz=math.sin(count))
        item.update()
    space.space_sort()


an = animation.Animation(2000, animation.flat, callback=_callback,
                         fps=60, repeat=-1, derivation=True)


tkt.Switch(space, (10, 10), command=lambda flag: an.start()
           if flag else an.stop())
# tkintertools-3d #


root.mainloop()
