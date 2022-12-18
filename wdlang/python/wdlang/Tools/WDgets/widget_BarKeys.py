from tkinter import Frame, Label

class BarKeys(Frame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def wd_update(self, __main__, values: dict):
    self.set_env(values)
    self.build({k:v for k,v in values.items() if "section_" in k})

    self.configure(bg = self.bd, bd = 1)

  def set_env(self, values: dict):
    self.bg = self.cget("bg")

    self.bd = values.get("bg")
    self.fg = values.get("fg")    or "black"
    self.ft = values.get("font")  or ("tkdefaultfont", 8)

  def build(self, sections : dict):
    for n, k in enumerate(sections):
      section_frame = Frame(self, bg = self.bg, name = k, width = 150)

      start = 0
      max_width = 0

      for name, key in sections[k].items():
        if key:
          text = "key > " + key
        else:
          text = ""
          key = ""

        value_frame = Label(section_frame, bg = self.bg, fg = self.fg, relief="flat", bd = 0, highlightthickness=0, text = name, anchor="w", font=self.ft)
        _key = Label(value_frame, bg = self.bg, fg = self.fg, relief="flat", bd = 0, highlightthickness=0, text = text, anchor="e", font=self.ft, name = key.lower())

        width = value_frame.winfo_reqwidth() + _key.winfo_reqwidth()
        max_width = max(width, max_width)

        _key.place(anchor="ne", relx = 0.98, rely = 0)
        value_frame.place(anchor="nw", x = 0, y = start, relwidth= 1, height=20)

        _key.bind("<ButtonRelease-1>", lambda Event: self.place_forget())
        value_frame.bind("<ButtonRelease-1>", lambda Event: self.place_forget())
        
        start += 20

      section_frame.columnconfigure(0, weight=1)

      section_frame.configure(height=start)
      section_frame.grid_propagate(False)
      section_frame.grid(sticky="we")

      if n != len(sections)-1:
        section_frame.grid_configure(pady = (0, 1))

  def set_keys(self, keys : dict) -> dict:
    __key_events__ : dict = {}

    for wid_name, functions in keys.items():
      for lb, ky in zip( self.nametowidget(wid_name).children.values(), functions):
        lb.bind("<Button-1>", ky)
        _key = list(lb.children.values())[0]
        
        if _key.winfo_name():
          key = _key.cget("text")[6:]

          if key == "del":
            key = "Delete"

          __key_events__[("small", key)] = ky

        _key.bind("<Button-1>", ky)

    return __key_events__
