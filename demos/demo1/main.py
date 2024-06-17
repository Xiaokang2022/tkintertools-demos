import random

import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.color as color
import tkintertools.core.constants as constants
import tkintertools.standard.shapes as shapes
import tkintertools.style as style
import tkintertools.three as three
import tkintertools.toolbox as toolbox

if toolbox.load_font("assets/fonts/LXGWWenKai-Regular.ttf"):
    constants.FONT = "霞鹜文楷"


def colorful(colortup: tuple[str, str]) -> None:
    first = color.str_to_rgb(colortup[0])
    second = color.str_to_rgb(colortup[1])
    for i, fill in enumerate(color.gradient(first, second, 1280, contoller=animation.smooth)):
        space.itemconfigure(colorlines[i], fill=color.rgb_to_str(fill))


def alert(text: str) -> None:
    hint._texts[0].set(text)
    animation.MoveWidget(
        hint, 500, (0, -130*space.ratios[1]), controller=animation.rebound, fps=60).start()
    animation.MoveWidget(
        hint, 500, (0, 130*space.ratios[1]), controller=animation.smooth, fps=60).start(delay=2000)


def move_right() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (900, 0),
                             controller=animation.smooth, fps=60).start()
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (900, 0),
                             controller=animation.rebound, fps=60).start(delay=100)


def move_left() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (-900, 0),
                             controller=animation.rebound, fps=60).start(delay=100)
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (-900, 0),
                             controller=animation.smooth, fps=60).start()


def switch_theme(flag: bool) -> None:
    style.set_color_mode("dark" if flag else "light")
    if flag:
        colorful(colortup=("#00BFA5", "#448AFF"))
    else:
        colorful(colortup=("#EEC1EB", "#B3C1EE"))


def get_random_int(min: int, max: int, interval: int) -> int:
    a = random.randint(min, -interval)
    b = random.randint(interval, max)
    return random.choice((a, b))


class DummyFrame(tkt.Widget):

    def __init__(
            self, master: tkt.Canvas, position: tuple[int, int], size: tuple[int, int], *, name: str | None = None, state: str = "normal", through: bool = False, animation: bool = True) -> None:
        super().__init__(master, position, size, name=name,
                         state=state, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self, radius=16)


class Space(three.Canvas):

    def space_sort(self) -> None:
        self._components.sort(key=lambda item: item._camera_distance())
        for item in self._components:
            self.lower(item.item, colorlines[-1])


root = tkt.Tk(title="Simple Project - Login Window")
root.alpha(0.93)
space = Space(root, zoom_item=True, free_anchor=True, keep_ratio="max")
space.place(width=1280, height=720, x=640, y=360, anchor="center")

style.customize_window(
    root,
    # style="acrylic",
    # hide_title_bar=True,
    # hide_button="all",
    # boarder_type="smallround",
)

colorlines = [space.create_line(i, 0, i, 720, width=3, fill="")
              for i in range(1280)]

switch_theme(style.get_color_mode() == "dark")

text3ds = []
geos = []

for i in range(8):
    outline = f"#{random.randint(0, (1 << 24)-1):06X}"
    geos.append(
        three.Cuboid(space, get_random_int(-300, 300, 0), get_random_int(-500, 500, 200), get_random_int(-300, 300, 100), 100, 100, 100,
                     color_outline_back=outline,
                     color_outline_down=outline,
                     color_outline_front=outline,
                     color_outline_left=outline,
                     color_outline_right=outline,
                     color_outline_up=outline),
    )
    outline = f"#{random.randint(0, (1 << 24)-1):06X}"
    text3ds.append(three.Text3D(space, (get_random_int(-300, 300, 0),
                                        get_random_int(-500, 500, 200), get_random_int(-300, 300, 100)), text="TKT", fill=outline),)


def _callback(_: float) -> None:
    """callback function of animation"""
    for item in geos[:5]:
        item.rotate(dy=-0.005, dz=0.01)
        item.update()
    for item in text3ds[:5]:
        item.rotate(dy=0.005, dz=0.01)
        item.update()
    for item in geos[5:]:
        item.rotate(dy=0.005, dz=-0.01)
        item.update()
    for item in text3ds[5:]:
        item.rotate(dy=-0.005, dz=0.01)
        item.update()
    space.space_sort()


an = animation.Animation(2000, animation.flat, callback=_callback,
                         repeat=-1, derivation=True)

login_widgets = [
    DummyFrame(space, (450, 70), (400, 560), name="Label"),
    tkt.Switch(space, (330+450, 20+70),
               default=style.get_color_mode() == "dark", command=switch_theme),
    tkt.CheckButton(space, (20+450, 20+70),
                    command=lambda flag: an.start() if flag else an.stop()),
    tkt.Information(space, (200+450, 80+70), text="Login",
                    fontsize=48, weight="bold"),
    tkt.Information(space, (30+450, 170+70), anchor="w", text="Account"),
    tkt.Entry(space, (25+450, 190+70), (350, 50)),
    tkt.Information(space, (30+450, 280+70), anchor="w", text="Password"),
    tkt.Entry(space, (25+450, 300+70), (350, 50)),
    tkt.Button(space, (25+450, 380+70), (350, 55),
               text="Login", name="", command=lambda: alert("Login Success!")),
    tkt.Information(space, (135+450, 470+70),
                    text="Do not have an account?", fontsize=18),
    tkt.UnderlineButton(space, (340+450, 470+70),
                        text="Sign up", fontsize=18, command=move_right)
]
login_widgets[-3]._shapes[0].styles = {"normal": {"fill": "#B3C1EE", "outline": "grey"},
                                       "hover": {"fill": "#EEC1EB", "outline": "grey"}}
login_widgets[-3].update()

signup_widgets = [
    DummyFrame(space, (450-900, 70), (400, 560), name="Label"),
    tkt.Information(space, (200+450-900, 80+70),
                    text="Sign up", fontsize=48, weight="bold"),
    tkt.Information(space, (30+450-900, 170+70), anchor="w", text="Account"),
    tkt.Entry(space, (25+450-900, 190+70), (350, 50)),
    tkt.Information(space, (30+450-900, 280+70), anchor="w", text="Password"),
    tkt.Entry(space, (25+450-900, 300+70), (350, 50)),
    tkt.Button(space, (25+450-900, 380+70), (350, 55),
               text="Sign Up", name="", command=lambda: alert("Sign Up Success!")),
    tkt.Information(space, (135+450-900, 470+70),
                    text="Already have an account?", fontsize=18),
    tkt.UnderlineButton(space, (350+450-900, 470+70),
                        text="Login", fontsize=18, command=move_left)
]
signup_widgets[-3]._shapes[0].styles = {"normal": {"fill": "#00BFA5", "outline": "grey"},
                                        "hover": {"fill": "#448AFF", "outline": "grey"}}
signup_widgets[-3].update()

hint = tkt.Label(space, (960, 730), (300, 100))

root.mainloop()
