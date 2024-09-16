import time

import tkintertools as tkt
import tkintertools.core.constants as constants
import tkintertools.media as media
import tkintertools.toolbox as toolbox

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    constants.FONT = "霞鹜文楷"


class FPSVideoCanvas(media.VideoCanvas):
    """添加显示 FPS 的功能"""

    def _refresh(self) -> None:
        global t
        now = time.time()
        cv.itemconfigure(fps, text=f"FPS: {int(1/(now-t)):02d}")
        t = now
        super()._refresh()


root = tkt.Tk(title="tkintertools-media")
t = time.time()
cv = FPSVideoCanvas(root, keep_ratio="min",
                    free_anchor=True, control=True, max_fps=60)
fps = cv.create_text(20, 20, text="FPS: 0", anchor="nw", fill="#0F0")
cv.place(width=1280, height=720, x=640, y=360, anchor="center")
cv.play("./assets/videos/Bad Apple.mp4")
root.mainloop()
