import tkinter

from importlib.machinery import SourceFileLoader
from .module import *

class App(tkinter.Tk):
  def __init__(self, list_templ, path_src):
    super().__init__()

    Contructor(self, list_templ, path_src)

    self.mainloop()

class Contructor:
  script = None
  templ = None
  mod_sync = Mod_sync()
  pool_nodes = []
  gen_root  = Gen_vals()

  def __init__(self, window : tkinter.Tk, list_templ : list, path_src):

    self.paths_root = Paths_root(path_src)

    for self.templ in list_templ[::-1]:
      self.script = self.templ.script

      for i in self.templ.widgets:
        self.others = i.others

        master_name, name = self.gen_root.gen_tkname(self.templ.name, i.name)
        master = window.nametowidget(master_name)

        self.create_widget(master, i , name)

      if self.script:
        self.pool_nodes.append([SourceFileLoader("func", str(self.script)).load_module().Main, window.nametowidget(self.templ.name)])
      
    del master, name
    del self.script, self.others, self.templ, list_templ

    for i in self.pool_nodes:
      self.mod_sync.push_node(*i)

    self.pool_nodes.clear()

  def load_presets(self, presets : list) -> dict:
    ret : dict = dict()

    for i in presets:
      ret.update(**self.gen_root.gen_darg(i.others))

    return ret

  def load_atributes(self, widget : tkinter.Widget, presets : dict, atributes : dict):
    atrb = {**presets, **self.gen_root.gen_darg(atributes)}

    widget.configure(**atrb)

  def run_commands(self, widget : tkinter.Widget, commands : dict):
    for (cmd, content) in commands.items():
      args  = [self.gen_root.gen_eval(i) for i in content.args or []]
      kwargs = {k : self.gen_root.gen_eval(v) for k, v in (content.kwargs or {}).items()}

      try:
        getattr(widget, cmd.strip())(*args, **kwargs)

      except:
        print(f"error in command {cmd} : ({args}, {kwargs}), widget : {widget} ")
        # to_do : push notify (warong)
      
  def create_widget(self, master : tkinter.Widget , class_widget, name):

    if str(master) == "." and name == ".":
      widget = master
    else:
      widget = self.gen_root.gen_type(class_widget.element_type)(master=master, name=name)

    self.load_atributes(widget, self.load_presets(class_widget.presets), class_widget.atributs)
    self.run_commands(widget, class_widget.commands)

    if "wdlang.Tools" in widget.__module__:
      widget.wd_update(self.paths_root, self.gen_root.gen_darg(self.others))

