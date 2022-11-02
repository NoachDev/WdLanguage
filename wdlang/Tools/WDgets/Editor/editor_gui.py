from tkinter import Canvas
from ..widget_selector_Box import Selector_Box

class Gui(Canvas):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def wd_update(self, __main__, values : dict):
    self.set_env(values)
    self.build()

  def set_env(self, values : dict):
    # self.df_bg  = self.cget("bg")

    self.bg     = values.get("bg") 
    self.fg     = values.get("fg")      or "white"
    
    self.font   = values.get("font")    or ("tkdefaultfont", 9)

    self.size_box = values.get("size_box") or 30

  def build(self):

    # select (and open config), move camera, zoom, forms

    self.box_tools = Selector_Box(self)
    self.box_tools.wd_update(None, {
      "bg"          : self.bg,
      "fg"          : self.fg,
      "text"        : " ",
      "mult"        : 10,
      "size_w"      : self.size_box,
      "size_h"      : self.size_box*5,
      "border"      : 6,
      "font"        : self.font,
      "txt_color"   : self.fg,
      "type_round"  : "custom",
      "is_canvas"   : [self, 10, self.size_box],
      # "function"    : lambda Event: self.change_to(text),
      "values_round": [15, 15, 15, 15]
      }
    )
    