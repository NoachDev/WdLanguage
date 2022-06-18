from Parser import WDParser
import pathlib

class Modify(dict):
  def __init__(self, path : str | pathlib.Path, vars : dict = {}, presets : list = [], customnfunctions : dict = {}):

    if type(path) == str:
      path = pathlib.Path(path)

    if path.is_absolute():
      src = path.absolute()
    else:
      src = pathlib.Path(path.name)

    self.sep_tk   = "."

    self.update(self.Reader(self.Organize_tknames(self.Get_file(path, src), self.sep_tk)))
  
  def Str_Py(self, strpy):
    try:
      return eval(strpy)
    except:
      ret = strpy

      if "[" in strpy and "]" in strpy or "(" in strpy and ")" in strpy:
        ret = [self.Str_Py(a.strip()) for a in strpy.replace("[", "").replace("]", "").replace("(", "").replace(")", "").split(sep = ",")]

      elif "{" in strpy and "}" in strpy:
        ret = {}

        for i in strpy.replace("(", "").replace(")", "").split(sep = ","):
          k, v = [a.strip() for a in i.split(sep = ":")]

          ret[k] = v
        
      return ret

  def Put_vars(self, wd_vars : dict , mdict : dict) -> dict :
    def check(value):
      if value in wd_vars:
        return self.Str_Py(wd_vars[value])

      return value

    for k, v in mdict.items():
      v = self.Str_Py(v)
      
      if type(v) == dict:
        mdict[k] = {kd : check(vd) for kd, vd in v.items()}

      elif type(v) == str:
        mdict[k] = check(v)

      elif type(v) != int and type(v) != float:
        mdict[k] = [check(a) for a in v]
    
    return mdict
  
  def Reader(self, dict_widg : dict, presets : dict = {}, wd_vars : dict = {}) -> dict:
    """
      use WDParser to read files for append widgets/atributes
    """

    data_widgets  = WDParser(dict_widg["file"])

    wd_vars.update(data_widgets["wd_vars"])
    presets.update({k : self.Put_vars(wd_vars, v) for k, v in data_widgets["presets"].items()})

    dict_widg["widget"] = {**wd_vars, **presets}
    undf_count          = 0

    for k, v in dict_widg["childrens"].items():
      dict_widg["childrens"][k].update(self.Reader(v, presets, wd_vars))
    
    for i in data_widgets["widgets"]:
      if i.get("self").get("tk_name") == "__master__":
        i["self"].pop("tk_name")

        dict_widg["widget"].update(i)
      else:
        dwidg = self.Put_vars(wd_vars, i)

        if "tk_name" in dwidg["self"]:
          name = dwidg["self"]["tk_name"]
        else:
          name  = f"undef{undf_count}"
          undf_count += 1

        dwidg["self"].pop("tk_name")

        dict_widg["childrens"].update({name: {**{"file" : dict_widg["file"], "script" : None}, **dwidg}})

    return dict_widg

  class ErrorWidget:
    def __init__(self, widname, master : str = None, file : str = None):
      print("Widget Error:")
      print(  "\t Widget Full name : ", widname)

      self.widname  = widname
      self.master   = master
      self.file     = file
    
    def matster_nfoud(self): 
      if self.master != None:
        print("\t Master not faund : ", self.master)
        
      if self.file != None:
        print("\t Widget file      : ", self.file)

      print()

  def Organize_tknames(self, tknames, src):
    """
      Put widgets to recursive mode with trre aspect

      dict to oranize -> {'.': {'file': PosixPath('Pages/__init__.wd'), 'script': PosixPath('Functions/__init__.py'), 'childrens': {}}, '.test': {'file': PosixPath('Pages/test/__init__.wd'), 'script': None, 'childrens': {}}}

      return {'.': {'file': PosixPath('Pages/__init__.wd'), 'script': PosixPath('Functions/__init__.py'), 'childrens': {'.test': {'file': PosixPath('Pages/test/__init__.wd'), 'script': None, 'childrens': {}}}}}
    """
    
    def get_masters(tklistname):
      """
      Function to locage widget ( .widget.widget1 )

      masters/name [. , widget , widget1]

      masters locage [., .widget, .widget.widget1]

      return masters/name

      """
      padd        = tklistname[0] # master to add name master 
      ntklistname = [padd]        # list of locages ( init with point )

      for i in tklistname[1:]:
        name = str(padd + self.sep_tk + i).replace(self.sep_tk*2, self.sep_tk)
        padd = name

        ntklistname.append(name)

      return ntklistname

    tree_len                = {}                # conacat for number of nambers
    rcs_widgets             = tknames.get(src)  # widgets of have listeds

    tknames.pop(src)                            # remove from tknames base of rcs_widgets

    #   get size and names from locages
    
    for i in tknames.keys():
      tt = i.split(sep = ".")                   # names 
      tl = len(tt)                              # size

      tt[0] = self.sep_tk                       # set the first name to main  

      if not tl in tree_len:                    # if not size with this key in tree_len create key with list as value
        tree_len[tl] = []
      
      tree_len[tl].append([tt, i])              # add names and locage to key size

    # organize tree_len to incrase
    call_keys = list(tree_len.keys())
    call_keys.sort()

    for ck in call_keys:
      v = tree_len.get(ck)

      for i in v:

        exist = True
        node  = rcs_widgets["childrens"]

        for a in get_masters(i[0])[1:-1]:
          if a in node:
            node = node.get(a)["childrens"]
          else:
            self.ErrorWidget(i[-1], a, str(tknames.get(i[-1])["file"])).matster_nfoud()
            exist = False

        if exist:
          node.update({i[-1] : tknames.get(i[-1])})

    return rcs_widgets
    
  def Get_file(self, path, src):
    """
      path  = locage of files

      src   = intial point of tkinetr names -> Pagees | .

      Functions:
        |---> __init__.py

      Pages:
        |---> __init__.wd
      
        |--->     test.wd

      return {'.': {'file': PosixPath('Pages/__init__.wd'), 'script': PosixPath('Functions/__init__.py'), 'childrens': {}}, '.test': {'file': PosixPath('Pages/test/__init__.wd'), 'script': None, 'childrens': {}}}
        
    """
    dfiles = {} # names and paths of files .wd and .py

    for i in path.iterdir():  # get files and dirs in path
      
      if i.is_file():         # get tkinter name if is file
        name      = str(i).replace(str(src), self.sep_tk).replace("/", self.sep_tk).replace("\\", self.sep_tk).replace(self.sep_tk*2, self.sep_tk).replace(".wd", "")
        pyscript  = pathlib.Path(str(i).replace(str(src), "Functions").replace(".wd", ".py")) # script python with same cordenates of wd fil but master dir is "Functions"

        if "__init__" in name:  # if file name is __init__ use name of parent dir
          name_replace = ".__init__"

          if i.parent.name == src.name:
            name_replace = "__init__" # if parent dir is src not use point

          name = name.replace(name_replace, "") # change name

        if not pyscript.exists():
          pyscript = None

        dfiles[name] = {"file" : i, "script" : pyscript, "childrens" : {}} # add tkname and file wd, python script locage

      else:
        dfiles.update(self.Get_file(i, src))

    return dfiles

if __name__ == "__main__":
  Modify("Pages")