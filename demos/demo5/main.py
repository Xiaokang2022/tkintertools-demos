import threading
import time
import tkinter.filedialog as filedialog

import matplotlib.figure as figure
import matplotlib.pyplot as pyplot
import numpy
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import tkintertools as tkt
import tkintertools.standard.dialogs as dialogs
import tkintertools.style as style
import tkintertools.toolbox.mpl as mpl


def get_offset(image1: Image.Image, image2: Image.Image, side: int) -> list[list[tuple[int, int]]]:
    """
    获取整个图片区域的偏移量数据

    * `image1`: 图片1
    * `imag2`: 图片2
    * `side`: 滑动窗口边长，单位像素
    """
    MAX_X = image1.size[0]//side - 1
    MAX_Y = image1.size[1]//side - 1
    MAX = MAX_Y*MAX_X

    best_offset = [[None]*MAX_Y for _ in range(MAX_X)]

    for X in range(MAX_X):
        for Y in range(MAX_Y):
            count = (X+1)*MAX_Y + Y+1
            pb.set(count/MAX)
            best_offset[X][Y] = plot_correlation(
                image1, image2, side, X, Y, plot=False)

    return best_offset


def plot_correlation(
    image1: Image.Image,
    image2: Image.Image,
    side: int,
    X: int,
    Y: int,
    *,
    plot: bool = True,
) -> tuple[int, int] | figure.Figure:
    """
    绘制互相关平面示意图

    * `image1`: 图片1
    * `image2`: 图片2
    * `side`: 滑动窗口边长，单位像素
    * `X`: 滑动窗口横向索引
    * `Y`: 滑动窗口纵向索引
    * `plot`: 是否绘制图片
    """
    half = side//2
    data_offset = [[-1]*(side+1) for _ in range(side+1)]

    x1, y1, x2, y2 = half + X*side, half + Y * \
        side, half + (X+1)*side, half + (Y+1)*side

    img1 = image1.crop((x1, y1, x2, y2))

    best_offset = 0, 0
    max_correlation = -1

    if not plot:  # 速度修正，把过大的结果删去
        half //= 4

    for dx in range(-half, half+1):
        for dy in range(-half, half+1):
            img2 = image2.crop((x1+dx, y1+dy, x2+dx, y2+dy))
            array_1 = numpy.array(img1).flatten()
            array_2 = numpy.array(img2).flatten()
            correlation = numpy.corrcoef(array_1, array_2)[0, 1]
            data_offset[half+dx][half+dy] = correlation
            if correlation > max_correlation:
                max_correlation = correlation
                best_offset = dx, dy
            elif correlation == max_correlation:
                if numpy.hypot(*best_offset) > numpy.hypot(dx, dy):
                    max_correlation = correlation
                    best_offset = dx, dy

    if plot:
        a._texts[0].set(f"最佳结果: {best_offset}, {max_correlation:.2f}")

        data_x = numpy.array([[i]*(side+1) for i in range(-half, half+1)])
        data_y = numpy.array([range(-half, half+1) for _ in range(side+1)])

        fig = figure.Figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_xlabel("dx")
        ax.set_ylabel("dy")
        ax.set_zlabel("Correlation")
        ax.set_title("Cross Correlation Coefficient Diagram")
        ax.plot_surface(data_x, data_y, numpy.array(
            data_offset), cmap="coolwarm")

        return fig

    return best_offset


def plot_quiver(data: list[list[tuple[int, int]]], *, export: bool = False) -> figure.Figure | None:
    """
    绘制速度矢量场

    * `data`: 速度矢量场数据
    * `export`: 是否导出图片对象
    """
    MAX_X = len(data)
    MAX_Y = len(data[0])
    data_U = [[None]*MAX_Y for _ in range(MAX_X)]
    data_V = [[None]*MAX_Y for _ in range(MAX_X)]

    for X in range(MAX_X):
        for Y in range(MAX_Y):
            data_U[X][Y] = data[X][Y][0]
            data_V[X][Y] = data[X][Y][1]

    U, V = numpy.array(list(zip(*data_U))), numpy.array(list(zip(*data_V)))
    M = numpy.hypot(U, V)

    if export:
        fig = figure.Figure()
        ax = fig.subplots()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Velocity Vector Field")
        q = ax.quiver(U, V, M)
        ax.quiverkey(q, 0.9, 0.9, 5, label="", coordinates='figure')
        return fig

    fig = pyplot.figure(figsize=(10, 5))
    ax = fig.subplots()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Vector Illustration")
    q = ax.quiver(U, V, M)
    ax.quiverkey(q, 0.9, 0.9, 5, label="", coordinates='figure')
    pyplot.show()


def set_calc_mode(flag: bool) -> None:
    """设置计算模式"""
    global MODE
    MODE = flag


def clear() -> None:
    """清除已有数据"""
    pb.set(0)
    toolbar.destroy()
    figure_canvas.destroy()


def open_images() -> None:
    """打开图片文件"""
    global FILE1, FILE2
    try:
        if filenames := filedialog.askopenfilenames():
            FILE1, FILE2, *_ = filenames
    except Exception as e:
        dialogs.TkMessage(e.__class__.__name__, e, title="遇到错误", icon="error")


def caculate() -> None:
    """根据模式计算数据"""
    global toolbar, figure_canvas
    c.disabled()
    clear()
    t = time.time()

    try:

        if MODE:  # 绘制互相关系数平面示意图
            fig = plot_correlation(
                Image.open(FILE1).crop(AREA),
                Image.open(FILE2).crop(AREA),
                int(SIDE.get()), *eval(INDEX.get()))
        else:  # 绘制速度矢量场
            fig = plot_quiver(get_offset(
                Image.open(FILE1).crop(AREA),
                Image.open(FILE2).crop(AREA),
                int(SIDE.get())), export=True)

        figure_canvas = mpl.FigureCanvas(fig, base_canvas)
        toolbar = mpl.FigureToolbar(
            figure_canvas, root, pack_toolbar=False)

        toolbar.pack(fill="x")
        figure_canvas.pack(expand=True, fill="both")

    except Exception as e:
        dialogs.TkMessage(e.__class__.__name__, e, title="遇到错误", icon="error")
    finally:
        c.disabled(False)
        b._texts[0].set(f"计算耗时: {time.time()-t:0.3f} s")


def show() -> None:
    """显示图片"""
    global toolbar, figure_canvas
    clear()

    try:
        figure_canvas = tkt.Canvas(base_canvas, zoom_item=True)
        x, y = root._size
        figure_canvas.create_image(
            x//2, y//2-60, image=ImageTk.PhotoImage(Image.open(FILE1).crop(AREA)))
        figure_canvas.create_text(
            x//2+1, 30+1, anchor="n", text=FILE1, fill="black")
        figure_canvas.create_text(
            x//2, 30, anchor="n", text=FILE1, fill="white")
        figure_canvas.pack(expand=True, fill="both")
    except Exception as e:
        dialogs.TkMessage(e.__class__.__name__, e, title="遇到错误", icon="error")


# constants.SYSTEM = "Windows11"
# constants.FONT = "霞鹜文楷"
mpl.set_mpl_default_theme(style.get_color_mode() == "dark")


MODE: bool = False  # 计算模式
# 取图片 (400, 800) ~ (2000, 1600) 的区域
AREA: tuple[int, int, int, int] = 400, 800, 2000, 1600
FILE1: str = ""  # 图一
FILE2: str = ""  # 图二

root = tkt.Tk((1600, 900), title="Matplotlib Project - PIV 图像分析")
root.minsize(1600, 900)
root.center()
base_canvas = tkt.Canvas(root, zoom_item=True)
base_canvas.place(width=1600, height=900)

fig = figure.Figure()

canvas = tkt.Canvas(base_canvas, height=120)
figure_canvas = mpl.FigureCanvas(fig, base_canvas)
toolbar = mpl.FigureToolbar(figure_canvas, root, pack_toolbar=False)

toolbar.pack(fill="x")
canvas.pack(side="bottom", fill="x")
figure_canvas.pack(expand=True, fill="both")

tkt.Information(canvas, (20, 10), text="滑动窗口边长", anchor="nw")
SIDE = tkt.Entry(canvas, (20, 50), (200, 50))
SIDE.set("24")

tkt.Information(canvas, (260, 10), text="滑动窗口索引", anchor="nw")
INDEX = tkt.Entry(canvas, (260, 50), (200, 50))
INDEX.set("(0, 0)")

pb = tkt.ProgressBar(canvas, (500, 15))
c = tkt.Button(canvas, (500, 50), (120, 50), text="计算", command=lambda: threading.Thread(
    target=caculate, daemon=True).start())

tkt.Button(canvas, (640, 50), (120, 50), text="显示", command=show)
tkt.Button(canvas, (780, 50), (120, 50), text="打开", command=open_images)

tkt.Information(canvas, (990, 30), text="明亮模式")
tkt.Information(canvas, (1170, 30), text="黑暗模式")
tkt.Information(canvas, (990, 80), text="速度矢量")
tkt.Information(canvas, (1170, 80), text="相关系数")

tkt.Switch(canvas, (1050, 15), 60, default=style.get_color_mode() == "dark",
           command=lambda b: style.set_color_mode("dark" if b else "light"))
tkt.Switch(canvas, (1050, 65), 60, command=set_calc_mode)

a = tkt.Information(canvas, (1270, 20),
                    text="最佳结果: (-, -), -1.00", anchor="nw")
b = tkt.Information(canvas, (1270, 60), text="计算耗时: 0.000 s", anchor="nw")

root.mainloop()
