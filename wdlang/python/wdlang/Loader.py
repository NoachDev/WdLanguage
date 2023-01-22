
import tkinter
import tkinter.ttk as ttk
# from .Tools import WDgets as Wd_gets

class App(tkinter.Tk):
  def __init__(self, list_templ):
    super().__init__()

    Contructor(self, list_templ)

    self.mainloop()

class Contructor:
  def __init__(self, window : tkinter.Tk, list_templ):
    for self.templ in list_templ:
      for i in self.templ.widgets:
        master, name = self.gen_tkname(self.templ.name, i.name)
        self.create_widget(window.nametowidget(master), i , name)
      
  def gen_tkname(self, master : str, widget : str):
    if widget == "__master__":
      index_l = master.rfind(".")+1
      return (master[0 : index_l], master[index_l :])

    elif master != ".":
      master += "."

    return (master, widget)
  
  def gen_type(self, type_name):
    if type_name != None:
      if type_name.find("ttk.") == True:
        return getattr(ttk, type_name.replace("ttk.", "").strip())

      # elif type_name.find("widg.") == True:
        # return getattr(Wd_gets, type_name.replace("widg.", "").strip())
      
      return getattr(tkinter, type_name.strip())

    return tkinter.Frame

  def load_presets(self, presets : list) -> dict:
    ret : dict = dict()

    for i in presets:
      ret.update(**{key : value.args.pop().strip() for (key, value) in i.others.items()})

    return ret

  def load_atributes(self, widget : tkinter.Widget, presets : dict, atributes : dict):
    atrb = {**presets, **{key : value.args.pop().strip() for (key, value) in atributes.items()}}

    widget.configure(**atrb)

  def run_commands(self, widget : tkinter.Widget, commands : dict):
    for (key, value) in commands.items():
      args  = value.args or []
      kwargs = value.kwargs or {}

      getattr(widget, key.strip())(*args, **kwargs)

  def create_widget(self, master : tkinter.Widget , class_widget, name):

    if str(master) == "." and name == "":
      widget = master
    else:
      widget = self.gen_type(class_widget.element_type)(master=master, name=name)

    self.load_atributes(widget, self.load_presets(class_widget.presets), class_widget.atributs)
    self.run_commands(widget, class_widget.commands)

    pass