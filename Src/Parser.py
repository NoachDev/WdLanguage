import pathlib

class WdReader(dict):
  def __init__(self, file : str | pathlib.Path, wd_vars : dict = {}, presets : dict = {}) -> dict:

    # simboly one, simboly two, type data, data function

    # type data
    #   0     = only args
    #   1     = only kwargs
    #   2     = args and kwargs
    #   none  = nothing
    
    self.sections_simbolys  = {
                        "comments" : ("*|", "|*", None, None),
                        "wd_vars" : ("-|", "|-", 0, self.wd_vars_func),
                        "presets" : (".|", "|.", 0, self.presets_func),
                        "widgets" : ("<|", "|>", 0, self.widgets_func)
                      }
    self.segments_simbolys  = {
                        "widgets" : {
                          "atrb"  : ("{|", "|}", 0, None),
                          "cmds"  : ("[|", "|]", 2, None)
                        },
                        "presets" : {
                          "layout" : ("_|", "|_", 2, None)
                        }
                      }

    self.undf_slvs          = {"list" : ("[", "]"), "tuple" : ("(", ")"), "dict" : ("{", "}"), "string" : ('"', '"')}

    self.sep_args_kwargs    = "|"
    self.sep_keynames_val   = ":"
    self.sep_data           = ","

    self.wd_vars    : dict  = wd_vars
    self.presets    : dict  = presets
    self.widgets    : dict  = {}
    self.undf_widg  : int   = 0

    with open(file, "r") as f:
      self.text_file = f.readlines()

    sections        : dict  = self.get_section(self.text_file, self.sections_simbolys)
    self.comments   : dict  = sections["comments"]

    self.update({"wd_vars" : self.wd_vars, "presets" : self.presets, "widgets" : self.widgets, "comments" : self.comments})
    
    # for k, v in self.items():
    #   print(k)
    #   print("\t", v)

  def get_text_inside(self, text : list, simboly_start : str, simboly_end : str) -> list:
    start_points, end_points, ret   = [], [], []
    count_start , count_end , rm    = 0, 0, 0

    for l, t in enumerate(text):

      while simboly_start in t or simboly_end in t:
        if simboly_start in t:
          count_start += 1
          charpoint = t.find(simboly_start)
          start_points.append((l, charpoint + rm))
          rm += charpoint+len(simboly_start)
          t = t[charpoint+len(simboly_start):]
        
        if simboly_end in t:
          count_end += 1
          charpoint = t.find(simboly_end)
          end_points.append((l, charpoint + rm))
          rm += charpoint+len(simboly_end)
          t = t[charpoint+len(simboly_end):]

        if count_start == count_end:
          index_start , position_start  = start_points[0]
          index_end   , position_end    = end_points[-1]

          text_inside = [text[a] for a in range(index_start, 1 + index_end)]

          if index_start == index_end:
            position_end -= position_start
          
          text_inside[0]  = text_inside[0]  [position_start + len(simboly_start):]
          text_inside[-1] = text_inside[-1] [: max(0, position_end)]

          ret.append({"text" : text_inside, "pointers" : (start_points[0], end_points[-1])})
          
          start_points  = []
          end_points    = []
          count_start   = 0
          count_end     = 0
      rm = 0

    return ret

  def get_section(self, text : list, section_simbolys : dict) -> dict:
    ret : dict = {}

    for name_section, ss_td in section_simbolys.items():
      simboly_section = ss_td[:2]
      type_data       = ss_td[2]
      function_data   = ss_td[3]

      ret[name_section] = []
      rm                = []

      for i in self.get_text_inside(text, *simboly_section):
        if type_data != None:
          ret[name_section].append(self.get_segments(i["text"], name_section, type_data))
        else:
          ret[name_section].append(i["text"])
        rm.append(i["pointers"])
      
      if function_data:
        function_data(ret[name_section])

      self.clear_text(text, rm[::-1], len(simboly_section[0]))

    return ret
  
  def get_segments(self, text : list, name_of_section : str, type_data : int,  simbolys_segments : dict = {}) -> dict:

    if name_of_section in self.segments_simbolys:
      simbolys_segments = self.segments_simbolys[name_of_section]
    
    segment_values    = self.get_section(text, simbolys_segments)
    data_lines_values = self.get_data_line(text, type_data)

    if simbolys_segments:
      return {"self" : data_lines_values, "segments" : segment_values}

    return data_lines_values
  
  def get_data_line(self, text : list, type_data : int) -> dict:
    ret : dict = {}
    start, end = None, None

    def simboly_out(line_text : str, sep_simboly : str) -> list:
      bsp : list = []

      for a in self.undf_slvs.values():
        for i in self.get_text_inside([line_text], *a):
          pointers = i["pointers"] 
          
          bsp.extend(list(range(pointers[0][-1], 1 + pointers[-1][-1])))

      return [l for l, t in enumerate(line_text) if t == sep_simboly and not l in bsp]

    def name_value(line_text : str):
      name      : str   = line_text[: line_text.find(self.sep_keynames_val)]
      value     : str   = line_text[len(name) + 2 :].strip()
      args      : list  = []
      kwargs    : dict  = {}
      val_start : int   = 0

      if simboly_out(value, self.sep_args_kwargs):
        args_values   : str = value[: simboly_out(value, self.sep_args_kwargs)[0]]
        kwargs_values : str = value[len(args_values) + 2 :]
      
      elif simboly_out(value, self.sep_keynames_val):
        kwargs_values : str = value
        args_values   : str = ""
      
      else:
        args_values   : str = value
        kwargs_values : str = ""

      for i in simboly_out(args_values, self.sep_data):
        args.append(self.str_to_py(args_values[val_start : i]))
        i += 1
        val_start = i
      
      if args_values:
        args.append(self.str_to_py(args_values[val_start:]))

      val_start   : int   = 0
      
      for i in simboly_out(kwargs_values, self.sep_data):
        val     : str     = kwargs_values[val_start : i]
        key_val : str     = val[: val.find(":")]

        kwargs  [key_val.strip()] = self.str_to_py(val[len(key_val) + 1 :])

        val_start = i + 1

      if kwargs_values:
        val     : str     = kwargs_values[val_start :]
        key_val : str     = val[: val.find(":")]
        kwargs  [key_val.strip()] = self.str_to_py(val[len(key_val) + 1 :])

      if len(args) == 1:
        args = args[0]

      if type_data == 0:
        ret[name.strip()] = args
      elif type_data == 1:
        ret[name.strip()] = kwargs
      else:
        ret[name.strip()] = {"args" : args, "kwargs" : kwargs}
    
    for l, t in enumerate(text):
      t = t.strip()

      if len(t) >= 1:
        k = simboly_out(t, self.sep_args_kwargs)

        if k:
          tm = t[: k[0]]
        else:
          tm = t

        if simboly_out(tm, self.sep_keynames_val):
          if end:
            name_value("".join([text[a] for a in range(start, end + 1)]).replace("\n", ""))

          start = l
          end   = l
        else:
          end   += 1
        
    name_value("".join([text[a] for a in range(start, end + 1)]).replace("\n", ""))

    return ret
  
  def str_to_py(self, text : str):
    text = text.strip()

    vglobals  : dict  = {}
    unrm_text : str   = text
    rmval     : int   = 0

    while True:
      try:
        return eval(text, vglobals)

      except NameError as e:
        old_name : str = str(e).split()[1].strip().removeprefix("'").removesuffix("'")

        if old_name in self.wd_vars:
          name = self.wd_vars[old_name]
        else:
          name = old_name

        vglobals[old_name] = name

      except SyntaxError as e:
        name      : str = str(repr(e)).split(sep = ",")[4].strip()
        old_name  : str = name.removeprefix("'").removesuffix("'")

        start     : int = unrm_text.find(old_name) + rmval
        end       : int = start + len(old_name)

        if name in self.wd_vars:
          name = f"'{self.wd_vars[name]}'"

        text = text[: start] + name + text[end:]

  def clear_text(self, text : list, pointers : list, slen) -> list:
    
    for i in pointers:
      start_index , start_point  = i[0]
      end_index   , end_point    = i[-1]

      text[start_index] = text[start_index] [: start_point - 1]
      text[end_index]   = text[end_index]   [end_point + slen :]


      for a in list(range(start_index + 1, end_index))[::-1]:
        text.pop(a)
      
    return text

  def wd_vars_func(self, wd_vars):
    for i in wd_vars:
      self.wd_vars.update(i)
  
  def presets_func(self, presets):
    for i in presets:
      name = i["self"]["preset"]

      i["self"].pop("preset")
      
      self.presets[name] = i
  
  def widgets_func(self, widgets):
    for i in widgets:
      
      if "tk_name" in i["self"]:
        name = i["self"]["tk_name"]
      else:
        name = f"widget{self.undf_widg}"
        self.undf_widg += 1

      i["self"].pop("tk_name")

      self.widgets[name] = i

if __name__ == "__main__":
  WdReader("Pages/__init__.wd", {"__master__" : "main"})