
"""
  get text of file wd

  broken in sections
    vars        -||-
    presets     .||.

    interface   <||>
      atrbutes  {||}
      commands  [||]
      customs   (||)
      
      widget    #//

    comments    *||*

    *undefined slaves
      lists     []
      dicts     {}
      tuples    ()
      strings   ""

"""

class WDParser(dict):
  def __init__(self, file):

    self.simboly_udf_slvs = [("[", "]"), ("(", ")"), ( "{", "}"), ('"', '"')]
    self.simboly_def_slvs = {"scmds" : ("[|", "|]"), "ccmds": ("(|", "|)"), "atrbs": ( "{|", "|}")}
    
    with open(file, "r") as f:
      self.text : list    = f.readlines()
    
    self.comm_bp = []
    self.vars_bp = []
    self.pres_bp = []
    self.widg_bp = []

    self["wd_vars"]  = {}
    self["presets"]  = []
    self["widgets"]  = []

    for p, i in self.Get_section(self.text, "-|", "|-", pointer=True):
      self["wd_vars"].update(self.Manage_segments(i))
      self.vars_bp.append(p)

    for p, i in self.Get_section(self.text, ".|", "|.", pointer=True):
      self["presets"].append(self.Manage_segments(i))
      self.pres_bp.append(p)

    for p, i in self.Get_section(self.text, "<|", "|>", pointer=True):
      self["widgets"].append(self.Sections_interface(i))

  def Sections_interface(self, text):
    interface_widget = {}

    for name, sp in self.simboly_def_slvs.items():
      for p, i in self.Get_section(text, sp[0], sp[1], pointer=True):
        interface_widget[name] = self.Manage_segments(i)
        self.Remove_from_list(text, [(p[0][0], p[1][0])])

    interface_widget["self"] = self.Manage_segments(text)
    return interface_widget

  def Remove_from_list(self, sourc : list, remove : list ) -> list:

    removed = []
    # print(remove)

    for i in remove:
      start = i[0]
      end   = i[-1]

      removed.extend(list(range(start, end+1)))
    
    removed.sort()
    removed.reverse()

    for i in removed:
      sourc.pop(i)

  def undefined_slaves(self, segments : list, sp : list | tuple, dict_segments : dict):
    # lines of data blocks
    rm      = []

    for sp1, sp2 in sp: 
      # get lines and text of block 
      for lp, t in self.Get_section(segments, sp1, sp2, pointer=True):
        # init of block
        start = lp[0][0]  # [[s, e], [s1, e1]] -> (s)

        # end of block
        end   = lp[-1][0] # [[s, e], [s1, e1]] -> (s1)

        # name of block
        name  = segments[start] # "test : ####"
        name  = name[:name.find(":")].strip() # "test : ####" -> test

        # values inside block
        value = sp1 + ("").join(t).replace("\n", "") + sp2 # #######\n####\n" -> (sp1)###########)(sp2)

        dict_segments[name] = value # push name and value to dict -> {name:value}
        
        rm.append((start, end))
      
    self.Remove_from_list(segments, rm)

  def Manage_segments(self, segments:list) -> dict:
    dict_segments = {}

    # insert and remove data blocks
    self.undefined_slaves(segments, self.simboly_udf_slvs, dict_segments)

    # line read
    for i in segments:
      name    = i[:i.find(":")].strip()   # get name
      value   = i[i.find(":")+1:].strip() # get value

      if len(name) >= 1:                  # if name not is line feed
        dict_segments[name] = value       # add value to dict
    
    return dict_segments

  def Get_section(self, txt : list, sp1 : str, sp2 : str, pointer : bool = False) -> list:
    """ 
        rerturn list
          text inside sections

          pointers (start, end)

        definede by sp1(string pointer 1) and (string pointer 2)

        pointer -> False, return list of text       * default

        pointer -> True , return list of pointers
    """
    
    sections      : list  = []
    pointers      : list  = []
    #                       start - > (line, pointer), end -> (line, pointer)
    point         : list  = []


    for line, text in enumerate(txt):
      #                   if not point has clear
      if sp1 in text and len(point) <= 0:
        # add poiunter start
        point.append((line, text.find(sp1)))
      
      #                  if have pointer start
      if sp2 in text and len(point) <= 1:
        # add poiunter end
        point.append((line, text.find(sp2)))
      
      # if have pointer to start and end, put point in pointers and clear point

      if len(point) >= 2:
        pointers.extend([point])
        # get values inside point[0][0](line start) to point[1][0](line end)
        lines_text      = txt[point[0][0] : 1 + point[1][0]]
        # cut the frist line to charcter sp1
        lines_text[0]   = lines_text[0][point[0][1] + len(sp1):]
        lines_text[-1]  = lines_text[-1][:point[1][1]]

        if sp2 in lines_text[-1]:
          lines_text[-1] = lines_text[-1].replace(sp2, "")

        sections.append(lines_text)
        
        point = []

    if pointer:
      return zip(pointers, sections)
    else:
      return sections

if __name__ == "__main__":
  print(WDParser("__init__.wd"))