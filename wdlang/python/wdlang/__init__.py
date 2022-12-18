from .wdlang import *

from pathlib import Path

import argparse, os, tkinter

Pages, Functions, Images, main_path = [None] * 4

class App(tkinter.Tk):
  def __init__(self):
    super().__init__()

    Constuct(".", self, Pages, Functions, Images)

    self.mainloop()

class main:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", '--Src_Directory', help="use to set Main Path of have foldera Pages Images and Funtions")
    parser.add_argument("-sf", '--Src_Functions', help="use to set folder Funtions")
    parser.add_argument("-si", '--Src_Images'   , help="use to set folder images")
    parser.add_argument("-sp", '--Src_Pages'    , help="use to set folder Pages")

    self.args = parser.parse_args()

    for i in [("Src_Directory", "main_path"), ("Src_Pages", "Pages"), ("Src_Functions", "Functions"),("Src_Images", "Images")]:
      self.append_path(*i, main_path)

    if not Pages.exists():
      raise ValueError(Pages, main_path)

    elif not Functions.exists():
      raise ValueError(Functions, main_path)

    App()

  def append_path(self, arg_name, path_name, main):
    # print("*\t", arg_name, path_name, main)
    val = getattr(self.args, arg_name)

    if val:
      globals().update(**{path_name : Path(val)})

    elif not main:
      global main_path
      main_path = Path(os.getcwd())

    elif main:
      up = Path(main_path.joinpath(path_name))

      if not up.exists():
        up = None
        
      globals().update(**{path_name : up})

__doc__ = wdlang.__doc__
if hasattr(wdlang, "__all__"):
	__all__ = wdlang.__all__