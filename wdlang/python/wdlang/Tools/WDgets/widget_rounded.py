from PIL import ImageTk, ImageDraw, Image
from tkinter import Canvas
from math import sqrt

class Rounded(Canvas):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def wd_update(self, __main__, values : dict):
    self.set_env(values)
    self.build()

  def set_env(self, values: dict):
    self.typ_rounded  = values.get("type_round")  or "single" # custom
    self.values_round = values.get("values_round")  # [0 , 10, 0, 20]

    self.bg           = values.get("bg")          or "red"

    try:
      self.bg = tuple([c//256 for c in self.winfo_rgb(self.bg)] + [255])
    except:
      pass

    self.is_canvas    = values.get("is_canvas")   or False
    
    self.fg           = values.get("fg")          or self.cget("fg")

    self.bd           = values.get("border")      or 3
    self.bd_color     = values.get("bd_color")    or "white"

    self.txt_color    = values.get("text_color")  or "white"


    self.font         = values.get("font")        or None

    self.size_w       = values.get("size_w")      or 30
    self.size_h       = values.get("size_h")      or 27

    self.text         = values.get("text")        or "Text here"
    self.text_pos     = values.get("text_pos")    or [self.size_w/2, self.size_h/2]
    self.text_anchor  = values.get("text_anch")   or "center"

    self.mt           = values.get("mult")        or 5
    self.function     = values.get("function")    or None


  def build(self):
    self.size_w, self.size_h = self.size_w * self.mt, self.size_h * self.mt

    self.src_image  = Image.new("RGBA", (self.size_w, self.size_h), (0 ,0 ,0 ,0))
    self.imagedrawn = ImageDraw.Draw(self.src_image)
    self.radios     = sqrt(min(self.size_w, self.size_h)**2 * 2) /2

    if self.typ_rounded == "single":
      self.imagedrawn.rounded_rectangle((1, 1, self.size_w - 1, self.size_h - 1), self.radios, fill = self.bg, outline=self.bd)

    else:
      self.image_nw = Image.new("RGBA", (self.size_w, self.size_h))
      self.image_ne = Image.new("RGBA", (self.size_w, self.size_h))
      self.image_sw = Image.new("RGBA", (self.size_w, self.size_h))
      self.image_se = Image.new("RGBA", (self.size_w, self.size_h))

      images = [self.image_nw, self.image_ne, self.image_sw, self.image_se]

      for r, i in zip(self.values_round, images):
        ImageDraw.Draw(i).rounded_rectangle([1, 1, self.size_w, self.size_h], r * self.radios /100, fill = self.bg, outline=self.bd_color, width=self.bd)

      self.src_image.paste(self.image_nw.crop([0, 0, self.size_w/2, self.size_h/2]), [0 ,0])
      self.src_image.paste(self.image_ne.crop([self.size_w/2, 0, self.size_w, self.size_h/2]), [int(self.size_w/2), 0])
      self.src_image.paste(self.image_sw.crop([0, self.size_h/2, self.size_w/2, self.size_h]), [0, int(self.size_h/2)])
      self.src_image.paste(self.image_se.crop([self.size_w/2, self.size_h/2, self.size_w, self.size_h]), [int(self.size_w/2), int(self.size_h/2)])

    self.size_w, self.size_h = int(self.size_w / self.mt), int(self.size_h / self.mt)
    
    self.image = ImageTk.PhotoImage(self.src_image.resize((self.size_w, self.size_h), Image.ANTIALIAS))

    if self.is_canvas:
      self.is_canvas[0].create_image(self.is_canvas[1], self.is_canvas[2], anchor = "nw", image = self.image, tags = "img_rounded")
      
      if self.text:
        self.is_canvas[0].create_text(*self.text_pos, anchor=self.text_anchor, justify="center", text=self.text, font=self.font, fill=self.txt_color, tags="text_rounded")
        self.is_canvas[0].tag_bind("text_rounded", "<Button-1>", self.function)
      
      # self.bind_image(0)
      self.is_canvas[0].tag_bind("img_rounded", "<Button-1>", self.bind_image)

    else:
      self.configure(width = self.size_w, height = self.size_h, bg = self.master.cget("bg"), bd = 0, highlightthickness=0, relief="flat")

      self.create_image(0, 0, anchor = "nw", image = self.image, tags = "img_rounded")
      
      if self.text:
        self.create_text(*self.text_pos, anchor=self.text_anchor, justify="center", text=self.text, font=self.font, fill=self.txt_color, tags="text_rounded")
        self.tag_bind("text_rounded", "<Button-1>", self.function)
      
      # self.bind_image(0)
      self.tag_bind("img_rounded", "<Button-1>", self.bind_image)
    
  def bind_image(self, Event):
    if self.src_image.getpixel((Event.x, Event.y))[-1] >= self.bg[-1]:
      if self.function:
        self.function(Event)