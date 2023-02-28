from . import Tools

import tkinter
import tkinter.ttk as ttk
from .Tools import WDgets as Wd_gets
from pathlib import Path 

class Mod_sync(dict):

  db_scripts = {}
  functions = Tools.Functions
  custom_widgets = Tools.WDgets

  def get_id_KeyName(self, name):
    if name == ".":
      return 0
    
    return len(name.split(".")) -1

  def push_node(self, func, widget):

    key = self.get_id_KeyName(str(widget))

    if self.db_scripts.get(key) == None:
      self.db_scripts[key] = {}
    
    self.db_scripts[key][str(widget.winfo_name())] = func(widget, self)

    pass

  def get_scripts(self, name : str):
    
    key = self.get_id_KeyName(name)
    return self.db_scripts.get(key).get(name)
  
class Paths_root:
  def __path_exist(self, path : Path) -> str:
    if path.exists():
      return path
    
    return None

  def __init__(self, path_src : Path) -> None:
    self.Src_images = self.__path_exist(path_src.joinpath("Images"))
    self.Src_fonts  = self.__path_exist(path_src.joinpath("Fonts"))

class Gen_vals:
  def gen_tkname(self, master : str, widget : str) -> str:
    if widget == "__master__":
      index_l = master.rfind(".")+1

      if master == ".":
        return ".", "."

      return master[: index_l], master[index_l:]

    return master, widget

  def gen_type(self, type_name):
    if type_name != None:

      if type_name.find("ttk.") == True:
        return getattr(ttk, type_name.replace("ttk.", "").strip())
      
      elif type_name.find("widg.") == True:
        module = Wd_gets

        for i in type_name.replace("widg.", "").strip().split("."):
          module = getattr(module, i)

        return module

      return getattr(tkinter, type_name.strip())

    return tkinter.Frame

  def gen_eval(self, value : str):
    vgbl = {}

    while True:
      try:
        return eval(value, vgbl)

      except NameError as e:
        vgbl[e.name] = e.name

      except SyntaxError as e:

        name  = e.text

        b = value[: e.end_lineno-1]
        a = value[e.end_offset+1 :]

        value =  b + f" \"{name}\" " + a


    pass

  def gen_darg(self, src : dict ) -> dict:
    return {k : self.gen_eval(v.args.pop()) for k, v in src.items()}
