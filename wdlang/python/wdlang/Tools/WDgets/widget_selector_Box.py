from tkinter import Frame
from .widget_rounded import Rounded

class Selector_Box(Rounded):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def wd_update(self, __main__, values : dict):
    self.set_env(values)
    self.build()

    self.__set_env__(values)
    self.__build__()

  def __set_env__(self, values : dict):
    self.post   = values.get("position")  or "fixed"
    self.widb   = values.get("widgets")   or ()
    self.selt   = values.get("selector")  or "box"
    self.pad_y  = values.get("pad_y")     or 0

  def __build__(self,):
    self.widg_in = Frame(self, ) 

    if self.post == "relat":
      # self.pad_y += 10
      # add new widget to move content

      self.widg_in.grid(row = 1, column=0, sticky="nswe", pady = self.pad_y)

    else:
      self.widg_in.grid(row = 1, column=0, sticky="nswe", pady = self.pad_y)

    for i in self.widb:
      if i[0] == "box":
        pass
      else:
        pass
      

    pass