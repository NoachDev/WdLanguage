from tkinter import Canvas, font, Frame, Entry

from pathlib import Path

from .widget_svg import Svg
from ..Functions import Event_Load

from PIL import Image, ImageTk
import numpy

class Tree_Lines(Canvas):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.events_nodes   : Event_Load  = Event_Load(button_events={("small", 1) : self.node_open_close})
    self.events_inside  : Event_Load  = Event_Load(button_events={("small", 1) : self.select})

    self.wid_inside     : list        = []

    self.ext_lwid       : dict        = {}

    self.ext_line       : bool        = False
    self.created        : bool        = False
    self.selection      : bool        = True

    self.padx           : int         = 15
    self.pady           : int         = 3
    
    self.directory      : None        = None
    self.current        : None        = None
    self.ent_current    : None        = None

  def wd_update(self, __main__, values : dict):

    self.color        : str           = self.cget("bg") 
    self.fill         : str           = values.get("fill") or "black"

    file_dir          : str   | None  = values.get("file_dir")
    self.type_file    : str   | None  = values.get("type_file")

    self.font         : str   | None  = values.get("font")
    self.font_type    : str           = values.get("font_type") or "normal"

    self.size_head    : int           = values.get("size_head") or 15
    self.font_size    : int           = values.get("font_size") or int(self.size_head/2)
    padx              : int   | None  = values.get("padx")
    pady              : int   | None  = values.get("pady")
    
    self.content      : dict  | None  = values.get("content")
    event_btn         : dict  | None  = values.get("event_btn")
    event_key         : dict  | None  = values.get("event_key")
    
    pad               : tuple | None  = values.get("pad")
    
    if file_dir:
      self.directory  : Path          = Path(file_dir)
    
    if values.get("ext_line"):
      self.ext_line   : bool          = True

    if pad:
      self.padx, self.pady            = pad
    
    else:
      if padx != None:
        self.padx = padx

      if pady != None:
        self.pady = pady

    if event_btn:
      self.global_btn_events(event_btn)

    else:
      self.events_nodes.append_button_events(values.get("event_btn_nd"))
      self.events_inside.append_button_events(values.get("event_btn_in"))

    if event_key:
      self.global_key_events(event_key)

    else:
      self.events_nodes.append_key_events(values.get("event_key_nd"))
      self.events_inside.append_key_events(values.get("event_key_in"))

    if self.directory:
      if not self.directory.exist():
        raise ValueError(file_dir)
      else:
        self.get_dir(self.directory, self.content)

    if self.content:
      self.__create__(self.content, (self.winfo_reqwidth(), self.winfo_reqheight() ) )

  def __create__(self, structure: dict, width : tuple, state = True) -> None:
    
    self.created    : bool        = True
    self.__main__   : Canvas      = Canvas(self, bd = 0, highlightthickness= 0, bg = self.color, width = width, height = self.size_head, name = "__main__")
    self.wid_nodes  : list        = [self.__main__]

    selected_color  : tuple       = (0,191,255) #(65,105,225)
    
    line_walpha     : numpy       = numpy.linspace(int(0.4*255),0, num=width, dtype=numpy.uint8,)
    line_whalpha    : numpy       = numpy.tile(line_walpha, (self.size_head, 1), )
    
    image_alpha     : Image       = Image.fromarray(line_whalpha)

    self.image_slct : Image       = Image.new("RGBA", (width, self.size_head), selected_color )

    self.font_text  : font.Font   = font.Font(self, family=self.font, weight = self.font_type, size=self.font_size)

    self.image_slct.putalpha(image_alpha)
    
    if self.ext_line:
      width -= self.padx

    self.append_in_node(self.__main__, structure, width, state=state)

    self.__main__ .grid()

    self.__main__.bind("<Configure>", self.resize_downlines)

  def __delete__(self, del_wid : Canvas, src : list):
    src.remove(del_wid.body)

    if del_wid.head in self.ext_lwid:
      self.ext_lwid.pop(del_wid)
      # self.remove_extline(del_wid)

    if del_wid.body.name is self.ent_current:
      self.ent_current = None

    if del_wid.head is self.current:
      self.current = None
    
    del_wid.destroy()

    if len(del_wid.master.children) <= 1:
      del_wid.master.grid_forget()
      self.remove_oc(del_wid.master.master.head)
    
  def append_in_node(self, node, value : dict, size_w, index = None, state = True, icon : None = None, node_ext : bool = False):

    padx  : int = self.padx
    lx    : int = size_w - self.padx

    if node.winfo_name() == "__main__":
      if not self.ext_line:
        padx : int = 0
      
      lx += self.padx

    if not node in self.wid_nodes:
      if node in self.wid_inside:
        self.wid_inside.remove(node)
        self.append_oc(node.master.head, change = True)

      self.wid_nodes.append(node)

    for text, inside in value.items():
      name            : str               = text.casefold()
      
      if name in node.children:
        continue
    
      image           : ImageTk           = ImageTk.PhotoImage(self.image_slct, (size_w, self.size_head))
      window, head, body                  = self.create_node(node, name, size_w, padx, state, index)
      window.name                         = text

      tx, y0, head.init_text              = self.font_text.measure(text), self.size_head/2, 0

      head.state_head : Svg               = Svg(head, bd = 0, highlightthickness = 0, bg = self.color, name = "open_close")
      values_hand     : dict              = {"image" : Path(__file__).parent.joinpath(">.svg"), "anchor" : "center", "stroke" : self.fill, "fill" : self.fill}

      head.state_head.__created__ : bool       = False

      head.image = image

      if state == True:
        values_hand["rotate"] = -90
        values_hand["tag"] = "down"
        
        head.state_head.create_image(0, 0, anchor = "nw", image = image, tags = "head", state = "hidden")
        head.state_head.wd_update(None, values_hand)

        if inside:
          self.append_in_node(body, inside, size_w, None , state)
          
          head.init_text += 12
          self.append_oc(head, head.state_head)

          self.events_nodes.Run_binds(head)
          self.events_nodes.Run_binds(head.state_head)

          if node_ext and self.ext_line:
            self.add_ext_line(head)
          
        else:
          self.wid_inside.append(body)
          self.events_inside.Run_binds(head)

      if padx >= 1:
        node.downline = node.create_line(4, 0 , 4, node.master.winfo_reqheight(), fill = self.fill, tags = "downline")
        
      head.create_image (0, 0, anchor = "nw" , image = image , state = "hidden"  , tags  = "head")
      head.create_text  (head.init_text, self.size_head / 2  , anchor = "w"  , text  = text  , fill  = self.fill , tags  = "text_head", font  = self.font_text , justify="left")
      head.create_line  (head.init_text + tx + 2 , y0, lx, y0, fill  = self.fill , tags  = "line_1")
      
      window.update()

  def create_node(self, canvas_src, name, size_w, padx, state, index : None | int = None) -> list[Canvas, Canvas, Canvas]:

    canvas_window                  : Canvas            = Canvas(canvas_src          , name = name    , bd = 0, highlightthickness= 0, bg = self.color)
    canvas_window.head             : Canvas            = Canvas(canvas_window       , name = "head"  , bd = 0, highlightthickness= 0, bg = self.color, width = size_w, height  = self.size_head)
    canvas_window.body             : Canvas            = Canvas(canvas_window       , name = "body"  , bd = 0, highlightthickness= 0, bg = self.color, width = size_w, height = 0)

    canvas_window.body.name        : Entry             = Entry (canvas_window.body  , name = "name"  , bd = 1, bg = self.color, width = size_w, borderwidth=1, highlightthickness=1, highlightbackground= self.fill, highlightcolor=self.fill, relief= "flat", font = (self.font, self.font_size, self.font_type), fg = self.fill)

    canvas_window.open             : bool              = state

    canvas_window.head.__icon__    : bool              = False
    
    canvas_window.body.name.bind("<Return>", lambda Event: self.config_ent(Event, canvas_window.body))

    if index:
      canvas_window.grid(row = index, column = 0, padx = (padx, 0), pady = (self.pady, 0), sticky="w")
    else:
      canvas_window.grid(padx = (padx, 0), pady = (self.pady, 0), sticky="w")

    canvas_window.head.grid(row = 0, column = 0, sticky="w")

    if state:
      canvas_window.body.grid(row = 1, column = 0, sticky="w")

    canvas_window.update()
    
    return canvas_window, canvas_window.head, canvas_window.body

  def get_dir(self, directory : Path, append_ : dict | None, show_hiden : bool = False, rp_init_ : bool = False ) -> dict:
    ret : dict = {}

    for i in directory.iterdir():
      name = i.name
      
      if name[0] == "." and not show_hiden or name == "__pycache__":
        continue

      if i.is_dir():
        aprt = self.get_dir(i, {}, show_hiden, rp_init_)

        if len(aprt) > 0:
          ret[name] = aprt

      else:
        if self.type_file and self.type_file in str(i):
          name = name.replace(self.type_file, "")
          
          if rp_init_ and name == "__init__":
            name = i.parent.name

          ret[name] = {}

    if append_ == None:
      append_ = ret
    else:
      append_.update(ret)

    return ret

  def append_oc(self, head : Canvas, sc : Svg | None = None, change : bool = False) -> bool:
    if not sc:
      sc = head.state_head
    
    if not sc.__created__:
      sc.place(x = 0, y = self.size_head / 5, anchor = "nw", width = 8, height= self.size_head / 2)

      if change :
        head.init_text += 12
        head.coords("text_head", head.init_text, self.size_head/2)
        
        x0, y0, x1, y1 = head.bbox("line_1")

        y = ( y0 + y1) / 2

        head.coords("line_1", x0 + head.init_text + 2, y, x1 , y)

      sc.__created__ = True

    return sc.__created__

  def remove_oc(self, head : Canvas, sc : Svg | None = None, change : bool = True) -> bool:
    if not sc:
      sc = head.state_head
    
    if sc.__created__:
      sc.place_forget()

      if change:
        head.init_text -= 12
        head.coords("text_head", head.init_text, self.size_head/2)
        x0, y0, x1, y1 = head.bbox("line_1")

        y = ( y0 + y1) / 2

        head.coords("line_1", x0 - 10, y, x1 - 10, y)
      
      sc.__created__ = False
      
    return sc.__created__
    
  def select(self, Event = None, head : None = None, change = True):
    #  hidden, normal

    if head:
      widget = head
    else:
      widget = Event.widget

    widget.focus_set()

    if self.current :
      self.current.itemconfig("head", state = "hidden")
      self.current.nametowidget("open_close").itemconfig("head", state = "hidden")
    
    if self.current != widget or not change:
      self.current    = widget

      widget.itemconfig("head", state = "normal")
      widget.nametowidget("open_close").itemconfig("head", state = "normal")

    else:
      self.current    : None  = None
    
    if self.ent_current:
      self.remove_entry(self.ent_current)

  def node_open_close(self, Event, node : None = None, change = True):
    if node:
      widget        : Canvas = node
      open_close    : Svg    = node.nametowidget("head.open_close")

    else:
      widget        : Canvas = Event.widget.master

      if widget.winfo_name() == "head":
        widget      : Canvas = widget.master
        open_close  : Svg    = Event.widget
      else:
        open_close    : Svg    = Event.widget.nametowidget("open_close")

    if change:
      if widget.open:
        open_close.update_svg(self.fill, "center", False, self.fill, 0, "up")

        widget.body.grid_forget()
        widget.update()

        for k, v in self.ext_lwid.items():
          if not k.winfo_ismapped():
            v.place_forget()

        widget.open = False
      
      else:
        for k, v in self.ext_lwid.items():
          if not v.winfo_ismapped():
            v.place(**v.coords)

        open_close.update_svg(self.fill, "center", False, self.fill, 0, "down")

        widget.body.grid()
        widget.update()

        widget.open = True

    if self.current != widget.nametowidget("head"):
      self.select("", head = widget.nametowidget("head"), change=change)
  
  def add_ext_line(self, node : Canvas):

    main = self.nametowidget("__main__")

    width , y = -5, self.size_head/2 

    width += node.winfo_rootx() - main.winfo_rootx()
    y += node.winfo_rooty() - main.winfo_rooty()

    line = Frame(self, bg=self.fill, bd = 1)
    line.coords = {"x" : 4, "y" : y, "width" : width, "height" : 1}
    line.place(**line.coords)

    self.ext_lwid[node] = line

  def resize_downlines(self, Event):
    for i in self.wid_nodes:
      i.coords("downline", 4, 0 , 4, i.master.winfo_reqheight())

  def config_ent(self, Event, locage):
    name              : str   = Event.widget.get().replace(" ", "_")
    size_w            : int   = Event.widget.winfo_reqwidth()

    if "." in name:

      return self.refuse_entry(Event.widget)

    self.remove_entry(Event.widget)
    
    if Event.widget.create:
      self.append_in_node(locage, {name: None}, size_w, None, True)
      self.select(None, locage.children.get(name).head)

    if Event.widget.func:
      Event.widget.func(locage.children.get(name).head)

  def remove_entry(self, ent: Entry):
    self.ent_current  : None  = None

    ent.delete(0, "end")
    ent.grid_forget()
    self.unrefuse_entry(ent)

    ent.master.configure(height = ent.master.winfo_reqheight() - ent.winfo_reqheight())
  
  def refuse_entry(self, entry):
    entry.configure(highlightbackground = "red", highlightcolor = "red")
    entry.update()

  def unrefuse_entry(self, entry):
    entry.configure(highlightbackground = self.fill, highlightcolor = self.fill)
    entry.update()

  def entry_append(self, locage : Canvas, func : None = None, create : bool = True) -> Entry:
    locage_name = locage.winfo_name()

    if locage_name == "head":
      locage = locage.master.body.name

    elif locage_name != "body":
      locage = locage.body.name

    if self.ent_current:
      self.ent_current.grid_forget()

    if self.current:
      self.select(None, self.current)

    locage.func = func
    locage.create = create
    self.ent_current = locage

    locage.grid(row = 0, column=0, sticky = "we", pady = (self.pady, 0), padx = (self.padx, 0))
    locage.bind("<Escape>", lambda Event: self.remove_entry(locage))
    row = 1

    for i in locage.master.children.values():
      i.grid(row = row)
      row += 1
      
    locage.focus_set()

    return locage
  
  def ni_delete(self, node : Canvas):
    if node.body in self.wid_nodes:
      self.__delete__(node, self.wid_nodes)
      self.events_nodes.del_binds(node.head)

    else:
      self.__delete__(node, self.wid_inside)
      self.events_inside.del_binds(node.head)

  def rename_ni(self, head : Canvas, name : str):
    head.itemconfig("text_head", text = name)
    tx = self.font_text.measure(name)

    x0, y0, x1, y1 = head.bbox("line_1")
    y = ( y0 + y1) / 2

    head.coords("line_1", head.init_text + tx + 2, y, x1 - x0, y)

  def global_btn_events(self, events : dict):
    self.events_nodes.append_button_events(events)
    self.events_inside.append_button_events(events)

  def global_key_events(self, events : dict):
    self.events_nodes.append_key_events(events)
    self.events_inside.append_key_events(events)
  