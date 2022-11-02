from multiprocessing import Event
from tkinter import Frame, font
from .widget_rounded import Rounded
import numpy as np
from PIL import Image, ImageTk

class Pages_rounded(Frame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def wd_update(self, __main__, values : dict) -> None:
    self.set_env(values)
    self.build()

  def set_env(self, values: dict) -> None:
    self.bg             = self.cget("bg")
    self.bg_selected    = [255, 255, 255, 30]

    try:
      self.bg_selected = tuple([c//256 for c in self.winfo_rgb(values.get("bg_selected"))] + [255])
    except:
      pass

    self.fg             = values.get("fg")      or "white"
    
    self.font           = values.get("font")    or ("tkdefaultfont", 9)

    self.font_text      = font.Font(self, family=self.font[0], size=self.font[-1])
    
    self.size_h         = values.get("size_h")  or 20 
    self.size_forget    = values.get("size_forget") or 10

    self.onclose        = values.get("onclose")

    self.columns        = 0
    self.selected       = None

    self.pages_content  = {}
    self.pages_forget   = {}

  def build(self) -> None:
    self.columnconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)

    self.Bar_pages = Frame(self, bg = self.bg, bd = 0, highlightthickness=0, relief="flat", height=0)
    self.content = Frame(self, bg = self.bg, bd = 0, highlightthickness=0, relief="flat")

    self.Bar_pages.grid(row = 0, column=0, sticky="nwe")
    self.content.grid(row = 1, column=0, sticky="nswe")

    self.content.columnconfigure(0, weight=1)
    self.content.rowconfigure(0, weight=1)

    self.append_page("test of widget red", Frame, bg = "#367486")
    self.append_page("test of widget green", Frame, bg = "#895738")

  def append_page(self, text, content, *args_content, **kwargs_content):
    
    cont = None

    if not text in self.pages_content:
      width = self.font_text.measure(text)

      page = Rounded(self.Bar_pages, name = text)
      cont = content(self.content, *args_content, **kwargs_content)
      
      cont.bind("<Control-Shift-T>", self.remember)
      cont.bind("<Control-Shift-W>", self.forget_page)

      cont.focus_set()

      page.wd_update(None, {
            "bg"          : self.bg,
            "fg"          : self.fg,
            "text"        : text,
            "mult"        : 10,
            "size_w"      : int(width + self.size_h * 2.3),
            "size_h"      : self.size_h,
            "text_pos"    : [self.size_h, self.size_h/2],
            "text_anch"   : "w",
            "border"      : 6,
            "font"        : self.font,
            "txt_color"   : self.fg,
            "type_round"  : "custom",
            "function"    : lambda Event: self.change_to(text),
            "values_round": [0, 30, 0, 0],
            }
        )

      page.create_text(int(width + self.size_h * 1.5), self.size_h/2, text="x", font = self.font, fill=self.fg, tags="close")
      page.tag_bind("close", "<Button-1>", self.forget_page)

      self.columns += 1

      data = np.array(page.src_image)
      data[(data == page.bg).all(axis = -1)] = self.bg_selected

      page.img_slc = ImageTk.PhotoImage(Image.fromarray(data, mode='RGBA').resize((int(width + self.size_h * 2.3), self.size_h), Image.ANTIALIAS))
      page.img_uns = page.image

      self.pages_content[text] = [page, cont]
    
    self.change_to(text)
    
    return cont

  def change_to(self, text):
    for t, p_c in self.pages_content.items():
      if text == t:
        if not p_c[0].winfo_ismapped():
          p_c[0].grid(row = 0, column=self.columns)

        if not p_c[-1].winfo_ismapped():
          p_c[-1].grid(row = 0, column = 0, sticky="nswe")
          self._select_(p_c[0])

        self.selected = text
      
      else:
        p_c[-1].grid_forget()
        self._unselect_(p_c[0])
  
  def forget_page(self, Event):
    if self.selected:
      if self.onclose:
        self.onclose()
      
      text = self.selected

      index = list(self.pages_content.keys()).index(text)-1
      page, content = self.pages_content.pop(text)

      page.grid_forget()
      content.grid_forget()

      self.columns -= 1

      if len(self.pages_forget) > self.size_forget:
        text_r = list(self.pages_forget.keys())[0]
        self.pages_content.pop(text_r)
        
        pr, cr = self.pages_forget.pop(text_r)

        pr.destroy()
        cr.destroy()

      self.pages_forget[text] = [page, content]

      if self.pages_content:
        rtext = list(self.pages_content.keys())[index]
        self.change_to(rtext)
      
  def remember(self, Event):
    if self.pages_forget:
      text = list(self.pages_forget.keys())[-1]
      self.columns += 1

      self.pages_content[text] = self.pages_forget.pop(text)

      self.change_to(text)

  def _select_(self, page):
    page.image = page.img_slc
    page.itemconfig("img", image=page.image)

  def _unselect_(self, page):
    page.image = page.img_uns
    page.itemconfig("img", image=page.image)