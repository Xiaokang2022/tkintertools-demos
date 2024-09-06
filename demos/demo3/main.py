import math

import tkintertools as tkt
import tkintertools.animation as animation


class LoginToplevel(tkt.Toplevel):
    """登录窗口"""

    def load_ui(self) -> None:
        """加载 UI"""
        canvas = tkt.Canvas(self)
        canvas.place(width=480, height=720)

        self.sub_title = tkt.Text(
            canvas, (240, 45), text="登录到你的账号", fontsize=36)

        canvas.create_oval(120, 90, 360, 330, outline="grey")
        canvas.create_text(240, 210, text="用户\n头像", fill="grey", font=30)

        self.account = tkt.InputBox(
            canvas, (40, 360), (400, 50), placeholder="请输入您的账号")
        self.password = tkt.InputBox(
            canvas, (40, 430), (400, 50), placeholder="请输入您的密码", show="●")
        self.an = tkt.Button(canvas, (40, 500), (190, 50),
                             text="注 册", command=self.animate)
        self.login = tkt.Button(canvas, (250, 500), (190, 50), text="登 录")
        self.password_verify = tkt.InputBox(
            canvas, (40, 500+300), (400, 50), placeholder="请再次输入您的密码", show="●")
        self.registry = tkt.Button(
            canvas, (40-300, 570), (190, 50), text="注 册")
        self.back = tkt.Button(canvas, (250+300, 570),
                               (190, 50), text="返 回", command=lambda: self.animate(True))

        self.forget = tkt.UnderlineButton(
            canvas, (140, 600), text="忘记密码", fontsize=20)
        self.sep = tkt.Text(canvas, (190, 600), text="|")
        self.find = tkt.UnderlineButton(
            canvas, (240, 600), text="找回账号", fontsize=20)
        self.sep_2 = tkt.Text(canvas, (290, 600), text="|")
        self.net = tkt.UnderlineButton(
            canvas, (340, 600), text="网络设置", fontsize=20)
        self.animation_lock = False  # 防熊

    def animate(self, back: bool = False) -> None:
        """执行相关动画"""
        if self.animation_lock:
            return
        self.animation_lock = True
        k = -1 if back else 1
        self.after(
            250, self.sub_title._texts[0].set, "登录到你的账号" if back else "注册新的账号")
        self.after(
            250, self.title, "登录" if back else "注册")
        animation.MoveWidget(self.sub_title, 500, (0, -80),
                             controller=animation.controller_generator(math.sin, 0, math.pi, map_y=False), fps=60,
                             end=lambda: self.__setattr__("animation_lock", False)).start()
        animation.MoveWidget(self.an, 500, (-300*k, 0),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.login, 500, (300*k, 0),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.registry, 500, (300*k, 0),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.back, 500, (-300*k, 0),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.forget, 500, (0, 100*k),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.sep, 500, (0, 100*k),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.find, 500, (0, 100*k),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.sep_2, 500, (0, 100*k),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.net, 500, (0, 100*k),
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.password_verify, 500, (0, -300*k),
                             controller=animation.smooth, fps=60).start()


root = tkt.Tk(title="Main Window")
root.center()

login = LoginToplevel(root, (480, 640), title="登录", grab=True)
login.resizable(False, False)
login.transient(root)
login.center()
login.load_ui()

root.mainloop()
