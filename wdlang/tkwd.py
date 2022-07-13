from . import Files
from .Tools import WDgets

import tkinter, tkinter.ttk

class Constuct:
  def __init__(self, Src_app_name : str, Src_app_method , Src_Pages : str, Src_functions : str, Src_images) -> None:
    self.masters      : dict  = {Src_app_name : Src_app_method}
    self.scripts_call : dict  = {}
    self.Src_Pages    : str   = Src_Pages
    self.Src_images   : str   = Src_images
    self.Src_functions: str   = Src_functions

    self.Create_widget(Src_app_method, Files.Files_structure(Src_Pages, Src_functions))

  def Create_widget(self, Src_method, widgets : dict) -> None:
    scripts      : dict = {}

    for tk_name, values in widgets.items():
      try:
        widg = Src_method.nametowidget(tk_name)

      except:
        master_name = tk_name[: max(1, tk_name.rfind("."))]

        if master_name in self.masters:
          master = self.masters[master_name]
        else:
          raise ValueError(master_name, self.masters)
        
        tk_type = values['self']['tk_type']
        name    : str = tk_name.replace(master_name+".", "").replace(master_name, "")
        module_call   = tkinter

        if "ttk." in tk_type:
          module_call = tkinter.ttk
          tk_type = tk_type.replace("ttk.", "")

        elif "widg." in tk_type:
          module_call = WDgets
          tk_type = tk_type.replace("widg.", "")
        
        widg = getattr(module_call, tk_type)(master, name = name)
        self.masters[tk_name] = widg

      atrbs : dict  = {}
      cmds  : dict  = {}

      if "presets" in values["self"]:
        prest_names = [values["self"]["presets"]]
        
        if type(prest_names) == str:
          prest_names = [prest_names]

        for a in prest_names:
          preset_val = widgets.varspresets["presets"][a]["self"]

          if "bg" in preset_val:
            preset_val["background"] = preset_val["bg"]
            preset_val.pop("bg")

          if "fg" in preset_val:
            preset_val["foreground"] = preset_val["fg"]

            preset_val.pop("fg")
          
          atrbs.update(preset_val)

      for a in values["segments"]["atrb"]:
        atrbs.update(a)

      if widg.__module__ == "tkinter.ttk":
        pass
      else:
        widg.configure(**atrbs)

      if "wdlang.Tools" in widg.__module__:
        widg.wd_update(self, values["self"])

      for a in values["segments"]["cmds"]:
        cmds.update(a)
      
      for cmd_name, ka in cmds.items():
        args = ka['args']

        if type(args) != list:
          args = [args]
          
        exec(f"widg.{cmd_name}(*args, **ka['kwargs'])")

      if values["script"]:    
        scripts[values["script"]] = widg
    
    self.Run_scripts(scripts)

  def Run_scripts(self, scripts):
    for k, v in scripts.items():
      self.scripts_call[v.winfo_name()] = k(v, self)
  
  def get_scripts(self, name):
    return self.scripts_call.get(name)
