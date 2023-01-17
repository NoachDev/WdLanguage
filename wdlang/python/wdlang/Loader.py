
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
      
  def get_presets(self):
    pass

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

  def load_atributes(self, widget : tkinter.Widget, atributes : list):
    atrb = {i.key : i.value.args.pop().strip() for i in atributes}

    widget.configure(**atrb)

  def load_presets(self, wdiget, presets):
    pass

  def run_commands(self, widget : tkinter.Widget, commands : list):
    for cmd in commands:
      key = cmd.key.strip()
      args  = cmd.value.args or []
      kwargs = cmd.value.kwargs or {}

      getattr(widget, key)(*args, **kwargs)

    pass

  def create_widget(self, master : tkinter.Widget , class_widget, name):

    if str(master) == "." and name == "":
      widget = master
    else:
      widget = self.gen_type(class_widget.element_type)(master=master, name=name)

    self.load_presets(widget, class_widget.presets)
    self.load_atributes(widget, class_widget.atributs)
    self.run_commands(widget, class_widget.commands)

    pass