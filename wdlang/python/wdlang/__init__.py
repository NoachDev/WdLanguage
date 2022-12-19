from .wdlang import *

import argparse, pathlib

# import tkinter
# from .tkwd import Constuct

# class App(tkinter.Tk):
#   def __init__(self):
#     super().__init__()

    # Constuct(".", self, Pages, Functions, Images)

    # self.mainloop()

class main:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", '--src_directory', help="use to set Main Path of have folder Pages and Funtions")

    args = parser.parse_args()

    if args.src_directory:
      main_path = args.src_directory
    else:
      main_path = pathlib.Path.cwd().as_posix()

    wdlang.dicovery_dir(main_path)

  def __repr__(self) -> str:
    return "\nwdlang end"

__doc__ = wdlang.__doc__

if hasattr(wdlang, "__all__"):
	__all__ = wdlang.__all__
