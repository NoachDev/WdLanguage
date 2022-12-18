from tkinter import Frame, Label
from ..widget_rounded import Rounded
from ..widget_pages_rounded import Pages_rounded

class Base(Frame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def wd_update(self, __main__, values : dict):
    self.set_env(values)
    self.build()

  def set_env(self, values : dict):

    self.bg     = self.cget("bg")
    self.fg     = values.get("fg")      or "white"
    
    self.font   = values.get("font")    or ("tkdefaultfont", 9)

    self.size_h = values.get("size_h")  or 20 
    self.size_w = values.get("size_w")  or 25

    self.size_box = values.get("size_box")or 30 

    self.back_f = values.get("back")
    self.next_f = values.get("next")

    self.pad_y  = 3

  def build(self):

    self.topt_bar = self.__top_bar__(self)
    self.__content__ = Pages_rounded(self, bg = self.bg, bd = 0, highlightthickness=0, relief="flat")

    self.__content__.wd_update(None, {
      "bg" : self.bg,
      "fg" : self.fg,
      "font" : self.font,
      "size_h" : self.size_h + self.pad_y,
    })

    self.bind("<Configure>",self.config_size )

  class __top_bar__(Rounded):
    def __init__(self, master):
      super().__init__(master)

      self.master = master
      self.place(x = 0, y =0 , relwidth = 1)

      self.bind("<Configure>", self.config_sizes)
      
      self.next_back(self, self.master.bg, self.master.fg, self.master.font, self.master.size_h, self.master.size_w, master.back_f, master.next_f, self.master.pad_y)

      self.search_bar = Rounded(self, bg = self.master.bg, bd = 0, highlightthickness=0, relief="flat", height = self.master.size_h)
      self.search_bar.place(y = self.master.pad_y, relx = 0.3)

      self.extn_t = Frame(self, bg = self.master.fg, bd = 0, highlightthickness=0, relief="flat", height=self.master.size_h)
      # self.extn_t.place( relx = 0.8, y = self.master.pad_y, relwidth=0.15)

    class next_back(Frame):
      def __init__(self, master, bg, fg, font, size_h, size_w, back_f, next_f, pad_y):
        super().__init__(master, bg = bg, bd = 0, highlightthickness=0, relief="flat", height=size_h)

        self.back = Label(self, bg = bg, bd = 0, highlightthickness=0, relief="flat", text="<", justify="center", font = font, fg = fg)
        self.next = Label(self, bg = bg, bd = 0, highlightthickness=0, relief="flat", text=">", justify="center", font = font, fg = fg)
        
        self.back.place(x = 0, y = 0, height = size_h, width = size_w)
        self.next.place(x = size_w, y = 0, height = size_h, width = size_w)

        self.back.bind("<Button-1>", back_f)
        self.next.bind("<Button-1>", next_f)

        self.back.bind("<Motion>", lambda Event: self.back.config(fg = "gray60"))
        self.next.bind("<Motion>", lambda Event: self.next.config(fg = "gray60"))

        self.back.bind("<Leave>", lambda Event: self.back.config(fg = fg))
        self.next.bind("<Leave>", lambda Event: self.next.config(fg = fg))

        self.place(x = 10, y = pad_y , width = size_w*2)

    def config_sizes(self, Event):
      self.wd_update(None, {
          "bg"          : self.master.bg,
          "fg"          : self.master.fg,
          "text"        : " ",
          "mult"        : 10,
          "size_w"      : Event.width,
          "size_h"      : self.master.size_h + self.master.pad_y*2,
          "border"      : 6,
          "txt_color"   : self.master.fg,
          "type_round"  : "custom",
          "values_round": [50, 50, 0, 0],
          }
      )

      self.search_bar.wd_update(None, {
        "bg"          : self.master.bg,
        "fg"          : self.master.fg,
        "text"        : " ",
        "mult"        : 10,
        "size_w"      : int(40 * Event.width / 100),
        "size_h"      : self.master.size_h,
        "border"      : 6,
        "txt_color"   : self.master.fg,
        "type_round"  : "custom",
        "values_round": [30, 30, 30, 30],
      })
  
  def config_size(self, Event):
    self.__content__.place(x = 0, y = self.size_h + self.pad_y*2, width = Event.width, height= Event.height - (self.size_h + self.pad_y*2))