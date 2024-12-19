import random

import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.core.configs as configs
import tkintertools.core.virtual as virtual
import tkintertools.standard.shapes as shapes
import tkintertools.style as style
import tkintertools.toolbox as toolbox

if toolbox.load_font("assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"


def alert(text: str) -> None:
    hint.texts[0].set(text)
    animation.MoveWidget(
        hint, 500, (0, -130*canvas.ratios[1]), controller=animation.rebound, fps=60).start()
    animation.MoveWidget(
        hint, 500, (0, 130*canvas.ratios[1]), controller=animation.smooth, fps=60).start(delay=2000)


def move_right() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (900*canvas.ratios[0], 0),
                             controller=animation.smooth, fps=60).start()
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (900*canvas.ratios[0], 0),
                             controller=animation.rebound, fps=60).start(delay=100)


def move_left() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (-900*canvas.ratios[0], 0),
                             controller=animation.rebound, fps=60).start(delay=100)
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (-900*canvas.ratios[0], 0),
                             controller=animation.smooth, fps=60).start()


def get_random_int(min: int, max: int, interval: int) -> int:
    a = random.randint(min, -interval)
    b = random.randint(interval, max)
    return random.choice((a, b))


class DummyFrame(virtual.Widget):

    def __init__(
        self,
        master: tkt.Canvas,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        state: str = "normal",
        through: bool | None = None,
        animation: bool | None = None,
    ) -> None:
        super().__init__(master, position, size, name=name,
                         state=state, through=through, animation=animation)
        if configs.Env.system == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self, radius=16)


root = tkt.Tk(title="Simple Project - Login Window")
canvas = tkt.Canvas(root, zoom_item=True, free_anchor=True, keep_ratio="max")
canvas.place(width=1280, height=720, x=640, y=360, anchor="center")

img = tkt.Image(canvas, (0, 0), image=tkt.PhotoImage(
    file=f"./assets/images/{style.get_color_mode()}.png"))

style.register_event(lambda theme: img.set(tkt.PhotoImage(
    file="./assets/images/%s.png" % ("light", "dark")[theme])))


login_widgets = [
    DummyFrame(canvas, (450, 70), (400, 560), name="Label"),
    tkt.Switch(canvas, (330+440, 20+70), default=style.get_color_mode() == "dark",
               command=lambda flag: style.set_color_mode("dark" if flag else "light")),
    tkt.Text(canvas, (200+450, 80+70), text="Login",
             fontsize=48, weight="bold", anchor="center"),
    tkt.Text(canvas, (30+450, 170+70), anchor="w",
             text="Account", fontsize=24),
    tkt.InputBox(canvas, (25+450, 190+70), (350, 50),
                 placeholder="Please enter your account"),
    tkt.Text(canvas, (30+450, 280+70), anchor="w",
             text="Password", fontsize=24),
    tkt.InputBox(canvas, (25+450, 300+70), (350, 50),
                 show="●", placeholder="Please enter your password"),
    tkt.Button(canvas, (25+450, 380+70), (350, 55),
               text="Login", name="", command=lambda: alert("Login Success!")),
    tkt.Text(canvas, (135+450, 470+70),
             text="Do not have an account?", fontsize=18, anchor="center"),
    tkt.UnderlineButton(canvas, (340+450, 470+70), anchor="center",
                        text="Sign up", fontsize=18, command=move_right)
]
login_widgets[-3].shapes[0].styles = {"normal": {"fill": "#B3C1EE", "outline": "grey"},
                                      "hover": {"fill": "#EEC1EB", "outline": "grey"}}
login_widgets[-3].update()

signup_widgets = [
    DummyFrame(canvas, (450-900, 70), (400, 560), name="Label"),
    tkt.Text(canvas, (200+450-900, 80+70),
             text="Sign up", fontsize=48, weight="bold", anchor="center"),
    tkt.Text(canvas, (30+450-900, 170+70),
             anchor="w", text="Account", fontsize=24),
    tkt.InputBox(canvas, (25+450-900, 190+70), (350, 50),
                 placeholder="Please enter your account"),
    tkt.Text(canvas, (30+450-900, 280+70), anchor="w",
             text="Password", fontsize=24),
    tkt.InputBox(canvas, (25+450-900, 300+70), (350, 50),
                 show="●", placeholder="Please enter your password"),
    tkt.Button(canvas, (25+450-900, 380+70), (350, 55),
               text="Sign Up", name="", command=lambda: alert("Sign Up Success!")),
    tkt.Text(canvas, (135+450-900, 470+70),
             text="Already have an account?", fontsize=18, anchor="center"),
    tkt.UnderlineButton(canvas, (350+450-900, 470+70), anchor="center",
                        text="Login", fontsize=18, command=move_left)
]
signup_widgets[-3].shapes[0].styles = {"normal": {"fill": "#00BFA5", "outline": "grey"},
                                       "hover": {"fill": "#448AFF", "outline": "grey"}}
signup_widgets[-3].update()

hint = tkt.Label(canvas, (960, 730), (300, 100))

root.mainloop()
