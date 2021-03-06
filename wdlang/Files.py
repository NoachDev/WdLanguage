from .Parser import WdReader 
from pathlib import Path

from importlib.machinery import SourceFileLoader

class Files_structure(dict):
  def __init__(self, Src_folder : str, Functions : None | str = None):
    self.Src_folder   : Path        = Path(Src_folder).absolute()
    self.Functions    : None | str  = Functions
    self.varspresets  : dict        = {"wd_vars" : {}, "presets" : {}}

    if not self.Functions:
      self.Functions = self.Src_folder.parent.joinpath("Functions")
    else:
      self.Functions = Path(self.Functions)

    self.update(self.Get_files(self.Src_folder))

  def Get_files(self, src : Path) -> dict :
    ret : dict = {}
    pathl : list = list(src.iterdir())
    pathl.sort()

    for i in pathl:
      if i.is_dir():
        ret.update(self.Get_files(i))
      else:
        name      = self.Transform_to_tkname(str(i))

        script    =  self.Functions.joinpath(i.parent.relative_to(self.Src_folder)).joinpath(i.name.replace(".wd", "") + ".py")

        if script.exists():
          script  = SourceFileLoader("func", str(script)).load_module().Main
        else:
          script  = None

        self.varspresets["wd_vars"]["__master__"] = name
        wdlang    = WdReader(i, **self.varspresets)

        ret.update({self.Chek_name(name, k) : {**v, "script" : None, "__master__" : name} for k, v in wdlang.widgets.items()})
        ret[name]["script"] = script 
        self.varspresets = {"wd_vars" : wdlang.wd_vars, "presets" : wdlang.presets}

    return self.Organize(ret)

  def Transform_to_tkname(self, widg) -> str:
    widg = widg.replace(".wd", "").replace("__init__", "")

    ret :str = widg[len(str(self.Src_folder)):].replace("/", ".").replace("\\", ".")

    if ret[-1] == ".":
      return ret[:max(1, len(ret)-1)]
    
    return ret
  
  def Chek_name(self, master : str, widget : str) -> str:
    ret : list = [*master.split(sep = ".")]
    
    widget = widget.replace(master, "" , 1)

    for i in widget.split(sep = "."):
      if not i in ret[-1]:
        ret.append(i)
      
    return ".".join(ret).replace("..", ".")
    
  def Organize(self, widgets : dict) -> dict:
    
    ret     : dict  = {}
    sep_len : dict  = {} 

    for i in [a.split(sep = ".") for a in widgets.keys()]:
      ln = len([ a for a in i if a != ""])

      if not ln in sep_len:
        sep_len[ln] = []

      sep_len[ln].append(i)


    inl : list      = list(sep_len.keys())
    inl.sort()

    for i in inl:
      for a in sep_len[i]:
        name = ".".join(a)
        ret[name] = widgets[name]

    return ret

if __name__ == "__main__":
  Files_structure("Pages")