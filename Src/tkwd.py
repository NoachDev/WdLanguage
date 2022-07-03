from Files import Files_structure
import tkinter
import tkinter.ttk

class Constuct:
  def __init__(self, Src_app_name : str, Src_app_method , Src_Pages : str, Src_functions : str) -> None:
    self.masters      : dict  = {Src_app_name : Src_app_method}
    self.scripts_call : dict  = {} 

    self.Create_widget(Src_app_method, Files_structure(Src_Pages, Src_functions))

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

        exec(f"widg = tkinter.{tk_type}(master, name = tk_name)")

      atrbs : dict  = {}
      cmds  : dict  = {}

      for a, c in zip(values["segments"]["atrb"], values["segments"]["cmds"]):
        atrbs.update(a)
        cmds.update(c)
      
      widg.configure(**atrbs)

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
