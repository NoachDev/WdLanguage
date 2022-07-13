from tkinter import Canvas

import cairosvg, io
from PIL import Image, ImageTk
from xml.etree import ElementTree

class svg(Canvas):
  def __init__(self, *args, **kwargs):
    super().__init__(*args)
    self.color_images : dict  = {}

  def wd_update(self, __main__, values):

    if "image" in values:
      path = self.get_file(values.get("image"), __main__.Src_images)
    else:
      raise ValueError(values, "image")

    if "anchor" in values:
      anchor : str  = values.get("anchor")
      
    else:
      anchor : str  = "center"

    if "fill" in values:
      fill   : str  = values.get("fill")

    else:
      fill   : str  = "black"

    if "pad" in values:
      self.padx, self.pady = values.get("pad")
      
    else:
      
      if "padx" in values:
        self.padx : int = int(values.get("padx"))
      else:
        self.padx : int = 0
      
      if "pady" in values:
        self.pady : int = int(values.get("pady"))
      else:
        self.pady : int = 0

    self.configure(bd = 0, highlightthickness=0)
    self.size_w, self.size_h  = self.winfo_reqwidth() - 1, self.winfo_reqheight() - 1
    self.ci = self.create_image(0, 0)

    tree      = ElementTree.parse(open(path, "r"))
    self.root = tree.getroot()

    self.update_svg(fill, anchor)
    self.bind("<Configure>", self.update_size)

  def Load_svg(self, root, fill : str, anchor : str) -> list:

    root.set("fill", fill)

    svg_paths : cairosvg  = cairosvg.svg2png(bytestring=ElementTree.tostring(root).decode("utf-8"))
    
    image     : Image     = Image.open(io.BytesIO(svg_paths))
    image_tk  : ImageTk   = ImageTk.PhotoImage(image.resize((self.size_w - self.padx, self.size_h - self.pady), Image.ANTIALIAS))

    return [image_tk] + self.get_posxy(anchor)

  def get_posxy(self, anchor):
    x , y = 0, 0

    if anchor == "center":
      x, y                = self.size_w / 2, self.size_h / 2
      
    elif anchor == "n":
      x       : float     = float(self.size_w/2)

    elif anchor == "e":
      x, y                = self.size_w, self.size_h/2

    elif anchor == "s":
      x, y                = self.size_w/2, self.size_h

    elif anchor == "w":
      y       : float     = float(self.size_h/2)

    elif anchor == "ne":
      x       : float     = float(self.size_w)
      
    elif anchor == "sw":
      y       : float     = float(self.size_h)

    elif anchor == "se":
      x, y                = self.size_w, self.size_h

    return [anchor, x, y]
  
  def set_image(self, color_name : str, anchor) -> None:
    img_tk, panchor, x, y  = self.color_images[color_name]

    if anchor and anchor != panchor:
      panchor, x, y = self.get_posxy(anchor)

    self.itemconfigure(self.ci, anchor = anchor, image = img_tk)
    self.coords(self.ci, x, y)

    self.image = img_tk
  
  def update_svg(self, fill, anchor = None, up : bool = False) -> None:
    self.current_fill = fill

    if not fill in self.color_images or up:
      self.color_images[fill] = self.Load_svg(self.root, fill, anchor)
    
    self.set_image(fill, anchor)

  def update_size(self, Event):
    self.size_w, self.size_h = Event.width, Event.height
    self.update_svg(self.current_fill, self.color_images[self.current_fill][1], up= True)

  def get_file(self, image, dft_image):
    if dft_image:
      path = dft_image.joinpath("svg").joinpath(image + ".svg")
      
      if path.exists():
        return path
      
      else:
        raise FileNotFoundError(path, "Not exist")
      
    else:
      raise FileNotFoundError(dft_image, "Not exist")