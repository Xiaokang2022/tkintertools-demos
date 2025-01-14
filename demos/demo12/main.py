import math

import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.theme as theme

root = tkt.Tk((476, 668))
root.center()
root.alpha(0.95)
theme.customize_window(root, hide_title_bar=True)
root.geometry(size=(476, 668))

cv = tkt.Canvas(auto_zoom=True)
cv.place(width=476, height=668)

photo = tkt.PhotoImage(file="assets/logo.png")

title = tkt.Text(cv, (238, 88), text="DEMO", fontsize=36, anchor="center")

a = animation.GradientItem(cv, title.texts[0].items[0], "fill", ("royalblue", "springgreen"), 2000, controller=lambda p: math.sin(p*math.pi), repeat=-1)
a.start()

tkt.Text(cv, (238, 388), text="小康", fontsize=26, anchor="center")
tkt.Image(cv, (238, 240), image=photo, anchor="center")

tkt.Button(cv, (96, 470), (284, 54), text="登 录").style.set(
    bg=("#00000000", "#2CDB83"), ol=("#2CDB83", "#2CDE85"), fg=("#2CDB83", "black"))

tkt.Env.system = "Windows10"

tkt.Button(cv, (476, 0), (42, 42), text="×", anchor="ne", fontsize=24, command=root.destroy).style.set(
    bg=("#00000000", "red"), ol=("#00000000", "red"))
tkt.Button(cv, (476-42-1, 0), (42, 42), text="-", anchor="ne", fontsize=24, command=root.destroy).style.set(
    bg=("#00000000", "#77777777"), ol=("#00000000", "#77777777"))
tkt.Image(cv, (14, 14), (28, 28), image=tkt.PhotoImage(file="assets/images/logo.png"))

tkt.UnderlineButton(cv, (140, 622), text="添加账号", anchor="sw")
tkt.Text(cv, (238, 622), text="|", anchor="s")
tkt.UnderlineButton(cv, (476-140, 622), text="移除账号", anchor="se")

root.at_exit(a.stop)
root.mainloop()
