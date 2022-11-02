import sys

sys.path.append("../../")

from wdlang.Tools.Functions.Animate import Motion, Size

class Main:
  def __init__(self, widget, tkwd):
    widget.geometry("1000x800+200+100")

    self.wid_t = widget.nametowidget("f_test")

    self.wid_t.wait_visibility()
    Motion(self.wid_t, 50, 130, 8, 0.05)
    Size(self.wid_t,self.wid_t.winfo_width(), self.wid_t.winfo_height(), 100, 100, 15, 0.05)