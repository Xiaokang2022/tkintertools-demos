import math
import random
import webbrowser

import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.color as color
import tkintertools.core.constants as constants
import tkintertools.core.virtual as virtual
import tkintertools.standard.dialogs as dialogs
import tkintertools.standard.features as features
import tkintertools.standard.shapes as shapes
import tkintertools.standard.texts as texts
import tkintertools.style as style
import tkintertools.toolbox as toolbox

root = tkt.Tk(title=f"{tkt.__name__} {tkt.__version__} - Basic Test")
root.center()
canvas = tkt.Canvas(root, zoom_item=True, keep_ratio="min", free_anchor=True)
canvas.place(width=1280, height=720, x=640, y=360, anchor="center")

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    constants.FONT = "LXGW WenKai"

constants.SIZE = -24

ORIGIN_SYSTEM = constants.SYSTEM

img = tkt.Image(canvas, (0, 0), image=tkt.PhotoImage(
    file=f"./assets/images/{style.get_color_mode()}.png"))

style.register_event(lambda theme: img.set(tkt.PhotoImage(
    file="./assets/images/%s.png" % ("light", "dark")[theme])))

"""
Data Card (RGBA - Experimental)
"""

_l = tkt.Label(canvas, (620, 390), (240, 310), name="")
_l._shapes[0].styles = {"normal": {"fill": "#448AFF33", "outline": "#448AFF"},
                        "hover": {"fill": "#00BFA533", "outline": "#00BFA5"}}
_l.update()

tkt.Text(canvas, (740, 430), text="— RGBA Card —", anchor="center")
tkt.UnderlineButton(canvas, (740, 490), text="Home Page", through=True, anchor="center",
                    command=lambda: webbrowser.open_new_tab("https://xiaokang2022.github.io/tkintertools/"))
tkt.UnderlineButton(canvas, (740, 530), text="GitHub (Source)", through=True, anchor="center",
                    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/tkintertools"))
tkt.UnderlineButton(canvas, (740, 570), text="Gitee (Mirror)", through=True, anchor="center",
                    command=lambda: webbrowser.open_new_tab("https://gitee.com/xiaokang-2022/tkintertools"))
tkt.UnderlineButton(canvas, (740, 610), text="GitCode (Mirror)", through=True, anchor="center",
                    command=lambda: webbrowser.open_new_tab("https://gitcode.com/Xiaokang2022/tkintertools"))
tkt.UnderlineButton(canvas, (740, 650), text="Bug Reports", through=True, anchor="center",
                    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/tkintertools/issues"))


"""
Here's the customization section
"""


class MyToplevel(tkt.Toplevel):
    """My Customized Toplevel"""

    def __init__(self, *args, **kw) -> None:
        constants.SYSTEM = ORIGIN_SYSTEM
        super().__init__(*args, size=(720, 405), **kw)
        self.transient(self.master)
        self.center(self.master)
        self.canvas = canvas = tkt.Canvas(self, free_anchor=True, expand="")
        canvas.place(width=720, height=405, x=360, y=202, anchor="center")
        canvas.create_rectangle(40, 40, 120, 120, dash="-", outline="grey")
        canvas.create_text(80, 25, text="Shape", fill="grey")
        self.s = canvas.create_text(80, 80, fill="red", justify="center")
        canvas.create_line(120, 80, 180, 80, 180, 160, 220,
                           160, fill="grey", arrow="last")
        canvas.create_rectangle(40, 160, 120, 240, dash="-", outline="grey")
        canvas.create_text(80, 145, text="Text", fill="grey")
        canvas.create_line(120, 202.5, 220, 202.5, fill="grey", arrow="last")
        canvas.create_rectangle(40, 280, 120, 360, dash="-", outline="grey")
        canvas.create_text(80, 265, text="Image", fill="grey")
        canvas.create_line(120, 320, 180, 320, 180, 240,
                           220, 240, fill="grey", arrow="last")
        canvas.create_rectangle(540, 40, 680, 120, dash="-", outline="grey")
        canvas.create_text(610, 25, text="Feature", fill="grey")
        self.f = canvas.create_text(610, 80, fill="purple")
        canvas.create_line(610, 120, 610, 202.5, 500,
                           202.5, fill="grey", arrow="last")
        canvas.create_rectangle(220, 70, 500, 350, dash=".", outline="red")
        canvas.create_text(360, 40, text="Widget", fill="red")

        self.shape: tkt.Shape = None
        self.text: tkt.Text = None
        self.image: tkt.Image = None
        self.feature: tkt.Feature = None
        self.style: dict = None
        self.widget: tkt.Widget = None

        tkt.Button(canvas, (585, 275), text="Clear", command=self.clear)
        tkt.Button(canvas, (585, 340), text="Generate", command=self.generate)

    def generate(self) -> None:
        """Generate a Widget randomly"""
        self.clear()
        self.shape = random.choice([shapes.Rectangle, shapes.Oval, shapes.Parallelogram, shapes.SharpRectangle,
                                   shapes.RegularPolygon, shapes.RoundedRectangle, shapes.SemicircularRectangle])
        self.feature = random.choice(
            [features.LabelFeature, features.ButtonFeature, features.Underline, features.Highlight])
        self.text = texts.Information
        self.widget = virtual.Widget(self.canvas, (300, 162), (120, 80))
        kw = {}
        match self.shape:
            case shapes.RegularPolygon: kw["side"] = random.randint(3, 9)
            case shapes.Parallelogram: kw["theta"] = random.uniform(-math.pi/6, math.pi/3)
            case shapes.RoundedRectangle: kw["radius"] = random.randint(4, 25)
            case shapes.SharpRectangle:
                kw["theta"] = random.uniform(math.pi/6, math.pi/3)
                kw["ratio"] = random.uniform(0, 1), random.uniform(0, 1)
        try:
            _s = self.shape(self.widget, **kw)
            self.shape = self.shape(self.widget, (-280, -120), **kw)
            _s.styles = self.shape.styles = {
                "normal": {"fill": self.randcolor(), "outline": self.randcolor()},
                "hover": {"fill": self.randcolor(), "outline": self.randcolor()},
                "active": {"fill": self.randcolor(), "outline": self.randcolor()},
            }
        except:
            self.canvas.itemconfigure(self.s, text="Param\nError")
        _t = self.text(self.widget, text="TKT")
        self.text = self.text(self.widget, (-280, 0), text="TKT")
        _t.styles = self.text.styles = {
            "normal": {"fill": self.randcolor()},
            "hover": {"fill": self.randcolor()},
            "active": {"fill": self.randcolor()},
        }
        self.canvas.itemconfigure(self.f, text=self.feature.__name__)
        self.feature = self.feature(self.widget)
        self.widget.update()

    def randcolor(self) -> str:
        """Get a random color string"""
        num = random.randint(0, (1 << 24) - 1)
        return f"#{num:06X}"

    def clear(self) -> None:
        """Clear Widget"""
        if self.widget is not None:
            self.widget.destroy()
            self.widget = None
        self.canvas.itemconfigure(self.s, text="")
        self.canvas.itemconfigure(self.f, text="")


"""
Below is the section of the style following system
"""

tkt.Switch(canvas, (50, 35), command=lambda b: (style.set_color_mode(
    "dark" if b else "light")), default=style.get_color_mode() == "dark")
tkt.CheckButton(canvas, (125, 35), command=root.fullscreen)


i = tkt.Text(canvas, (440, 50),
             text="tkintertools 3: a Brand New UI Framework", fontsize=26, name="", anchor="center")

tkt.HighlightButton(canvas, (790, 50), text="Get More!", command=MyToplevel, anchor="center")

tkt.Button(canvas, (900, 405), (360, 50),
           text="Call a Nested Window", command=lambda: toolbox.embed_window(tkt.Toplevel(), root))
tkt.Button(canvas, (900, 465), (360, 50),
           text="Call a Font Chooser", command=dialogs.TkFontChooser)
tkt.Button(canvas, (900, 525), (360, 50),
           text="Call a Color Chooser", command=dialogs.TkColorChooser)

info = tkt.Button(canvas, (900, 585), (175, 50), name="",
                  text="Information", command=lambda: dialogs.TkMessage(icon="info"))
info._shapes[0].styles = {"normal": {"fill": "skyblue", "outline": "grey"}}
info.update()
question = tkt.Button(canvas, (900 + 185, 585), (175, 50), name="",
                      text="Question", command=lambda: dialogs.TkMessage(icon="question"))
question._shapes[0].styles = {"normal": {
    "fill": "lightgreen", "outline": "grey"}}
question.update()
warning = tkt.Button(canvas, (900, 645), (175, 50), name="",
                     text="Warning", command=lambda: dialogs.TkMessage(icon="warning"))
warning._shapes[0].styles = {"normal": {"fill": "orange", "outline": "grey"}}
warning.update()
error = tkt.Button(canvas, (900 + 185, 645), (175, 50), name="",
                   text="Error", command=lambda: dialogs.TkMessage(icon="error"))
error._shapes[0].styles = {"normal": {"fill": "red", "outline": "grey"}}
error.update()


random_color = f"#{random.randint(0, (1 << 24) - 1):06X}"
contast_color = color.rgb_to_str(
    color.contrast(color.str_to_rgb(random_color)))


animation.GradientItem(canvas, i._texts[0].items[0], "fill", 2000, (random_color, contast_color),
                       repeat=-1, controller=lambda x: math.sin(x*math.pi)).start()


"""
Here's the part for customizing the system
"""


constants.SYSTEM = "Windows11"

tkt.Label(canvas, (50, 100), (120, 50), text="Label")
tkt.Label(canvas, (180, 100), (120, 50), text="Label").disabled()
l = tkt.Label(canvas, (310, 100), (120, 50), text="Label", name="")
l._shapes[0].styles = {"normal": {"fill": "", "outline": "#5E8BDE"},
                       "hover": {"fill": "", "outline": "#FFAC33"}}
l._texts[0].styles = {"normal": {"fill": "#5E8BDE"},
                      "hover": {"fill": "#FFAC33"}}
l.update()

tkt.Button(canvas, (50, 180), (120, 50), text="Button")
tkt.Button(canvas, (180, 180), (120, 50), text="Button").disabled()
b = tkt.Button(canvas, (310, 180), (120, 50), text="Button", name="")
b._shapes[0].styles = {"normal": {"fill": "#5E8BDE", "outline": "#5E8BDE"},
                       "hover": {"fill": "#CCCC00", "outline": "#CCCC00"},
                       "active": {"fill": "#FFAC33", "outline": "#FFAC33"}}
b.update()

pb1 = tkt.ProgressBar(canvas, (50, 260), (380, 8))
pb2 = tkt.ProgressBar(canvas, (50, 280), (380, 8), name="")

pb2._shapes[0].styles = {"normal": {"fill": "", "outline": ""}}
pb2._shapes[1].styles = {"normal": {"fill": "gold", "outline": "gold"}}
pb2._shapes[1].disappear()
pb2.update()

animation.Animation(2000, animation.smooth, callback=pb1.set,
                    fps=60, repeat=math.inf).start(delay=1500)
animation.Animation(2000, animation.smooth, callback=pb2.set,
                    fps=60, repeat=math.inf).start(delay=1000)

pb3 = tkt.ProgressBar(canvas, (50, 315), (380, 20))
pb4 = tkt.ProgressBar(canvas, (50, 350), (380, 20), name="")

pb4._shapes[0].styles = {"normal": {"fill": "", "outline": "grey"}}
pb4._shapes[1].styles = {"normal": {"fill": "pink", "outline": "pink"}}
pb4._shapes[1].disappear()
pb4.update()

animation.Animation(2000, animation.smooth, callback=pb3.set,
                    fps=60, repeat=math.inf).start(delay=500)
animation.Animation(2000, animation.smooth, callback=pb4.set,
                    fps=60, repeat=math.inf).start()

tkt.CheckButton(canvas, (50, 390))
tkt.Text(canvas, (165, 390 + 15), text="CheckButton", anchor="center")
tkt.RadioButton(canvas, (250, 390 + 3))
tkt.Text(canvas, (355, 390 + 15), text="RadioButton", anchor="center")
tkt.Text(canvas, (460, 390 + 15), text="Off", anchor="center")
tkt.Switch(canvas, (490, 390))
tkt.Text(canvas, (580, 390 + 15), text="On", anchor="center")

tkt.CheckButton(canvas, (50, 440), default=True).disabled()
tkt.Text(canvas, (165, 440 + 15), text="CheckButton",
         anchor="center").disabled()
tkt.RadioButton(canvas, (250, 440 + 3), default=True).disabled()
tkt.Text(canvas, (355, 440 + 15), text="RadioButton",
         anchor="center").disabled()
tkt.Text(canvas, (460, 440 + 15), text="Off", anchor="center").disabled()
tkt.Switch(canvas, (490, 440), default=True).disabled()
tkt.Text(canvas, (580, 440 + 15), text="On", anchor="center").disabled()

tkt.InputBox(canvas, (50, 595 - 5), (270, 50), placeholder="Placeholder")
e = tkt.InputBox(canvas, (50, 655 - 5), (270, 50))
e.set("Input")
e.disabled()

constants.SYSTEM = "Windows10"

tkt.Label(canvas, (50 + 410, 100), (120, 50), text="Label")
tkt.Label(canvas, (180 + 410, 100), (120, 50), text="Label").disabled()
tkt.Label(canvas, (310 + 410, 100), (120, 50), text="Label", name="")

tkt.Button(canvas, (50 + 410, 180), (120, 50), text="Button")
tkt.Button(canvas, (180 + 410, 180), (120, 50), text="Button").disabled()
b2 = tkt.Button(canvas, (310 + 410, 180), (120, 50), text="Button", name="")

b2._shapes[0].styles = {"normal": {"fill": "", "outline": ""},
                        "hover": {"fill": "yellow", "outline": "red"}}
b2._texts[0].styles = {"normal": {"fill": ""},
                       "hover": {"fill": "black"}}
b2.update()

pb5 = tkt.ProgressBar(canvas, (50 + 410, 260), (380, 8))
pb6 = tkt.ProgressBar(canvas, (50 + 410, 280), (380, 8), name="")

pb6._shapes[0].styles = {"normal": {"fill": "orange", "outline": "orange"}}
pb6._shapes[1].styles = {"normal": {"fill": "red", "outline": "red"}}
pb6._shapes[1].disappear()
pb6.update()

animation.Animation(2000, animation.flat, callback=pb5.set,
                    fps=60, repeat=math.inf).start()
animation.Animation(2000, animation.flat, callback=pb6.set,
                    fps=60, repeat=math.inf).start(delay=500)

pb7 = tkt.ProgressBar(canvas, (50 + 410, 315), (380, 20))
pb8 = tkt.ProgressBar(canvas, (50 + 410, 350), (380, 20), name="")

pb8._shapes[0].styles = {"normal": {"fill": "", "outline": ""}}
pb8._shapes[1].styles = {"normal": {"fill": "purple", "outline": "cyan"}}
pb8._shapes[1].disappear()
pb8.update()

animation.Animation(2000, animation.flat, callback=pb7.set,
                    fps=60, repeat=math.inf).start(delay=1000)
animation.Animation(2000, animation.flat, callback=pb8.set,
                    fps=60, repeat=math.inf).start(delay=1500)

tkt.CheckButton(canvas, (50, 490))
tkt.Text(canvas, (165, 490 + 15), text="CheckButton", anchor="center")
tkt.RadioButton(canvas, (250, 490 + 3))
tkt.Text(canvas, (355, 490 + 15), text="RadioButton", anchor="center")
tkt.Text(canvas, (460, 490 + 15), text="Off", anchor="center")
tkt.Switch(canvas, (490, 490))
tkt.Text(canvas, (580, 490 + 15), text="On", anchor="center")

tkt.CheckButton(canvas, (50, 540)).disabled()
tkt.Text(canvas, (165, 540 + 15), text="CheckButton",
         anchor="center").disabled()
tkt.RadioButton(canvas, (250, 540 + 3)).disabled()
tkt.Text(canvas, (355, 540 + 15), text="RadioButton",
         anchor="center").disabled()
tkt.Text(canvas, (460, 540 + 15), text="Off", anchor="center").disabled()
tkt.Switch(canvas, (490, 540)).disabled()
tkt.Text(canvas, (580, 540 + 15), text="On", anchor="center").disabled()

tkt.InputBox(canvas, (50 + 280, 595 - 5), (270, 50))
tkt.InputBox(canvas, (50 + 280, 655 - 5), (270, 50)).disabled()

i1 = tkt.Text(canvas, (1210, 20), text="0%", anchor="nw")
tkt.Slider(canvas, (900, 20), (300, 30),
           command=lambda k: (i1.set(f"{int(k*100):d}%"), root.alpha(k))).set(0.95)
tkt.Slider(canvas, (900, 60), (300, 30)).disabled()

tkt.IconButton(canvas, (900, 200), text="C", image=tkt.PhotoImage(
    file="./assets/images/logo-C.png"))
tkt.IconButton(canvas, (980, 200), text="C++", image=tkt.PhotoImage(
    file="./assets/images/logo-C++.png"))
tkt.IconButton(canvas, (1090, 200), text="C#", image=tkt.PhotoImage(
    file="./assets/images/logo-C#.png"))

tkt.IconButton(canvas, (900, 300), text="Minecraft", image=tkt.PhotoImage(
    file="./assets/images/logo-Minecraft.png"))
tkt.IconButton(canvas, (1070, 300), text="Ubuntu", image=tkt.PhotoImage(
    file="./assets/images/logo-Ubuntu.png"))

constants.SYSTEM = "Windows11"

i2 = tkt.Text(canvas, (1210, 100), text="0%", anchor="nw")
tkt.Slider(canvas, (900, 100), (300, 30),
           command=lambda k: i2.set(f"{int(k*100):d}%")).set(0.5)
tkt.Slider(canvas, (900, 140), (300, 30)).disabled()

tkt.IconButton(canvas, (900, 250), text="Python", image=tkt.PhotoImage(
    file="./assets/images/logo-Python.png"))
tkt.IconButton(canvas, (1040, 250), text="Java", image=tkt.PhotoImage(
    file="./assets/images/logo-Java.png"))
tkt.IconButton(canvas, (1150, 250), text="TKT", image=tkt.PhotoImage(
    file="./assets/images/logo.png"))

tkt.IconButton(canvas, (900, 350), text="Windows", image=tkt.PhotoImage(
    file="./assets/images/logo-Windows.png"))
tkt.IconButton(canvas, (1060, 350), text="Linux", image=tkt.PhotoImage(
    file="./assets/images/logo-Linux.png"))

root.mainloop()
