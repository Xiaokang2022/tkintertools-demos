import tkintertools as tkt
import tkintertools.core.constants as constants
import tkintertools.media as media
import tkintertools.toolbox as toolbox

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    constants.FONT = "LXGW WenKai"

root = tkt.Tk(title=f"tkintertools-media v{media.__version__}")
cv = media.VideoCanvas(root, keep_ratio="min", free_anchor=True, controls=True)
cv.place(width=1280, height=720, x=640, y=360, anchor="center")
cv.open("./assets/videos/Bad Apple.mp4")
root.mainloop()
