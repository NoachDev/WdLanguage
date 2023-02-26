from .wdlang import *

import argparse, pathlib
from .Loader import App

# import tkinter
# from .tkwd import Constuct



class main:
  def __init__(self) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", '--src_directory', help="use to set Main Path of have folder Pages and Funtions")

    args = parser.parse_args()

    if args.src_directory:
      main_path = pathlib.Path(args.src_directory)
    else:
      main_path = pathlib.Path.cwd()
      
    App(wdlang.dicovery_dir(main_path.as_posix()), main_path)

  def __repr__(self) -> str:
    return "\nwdlang end"


__doc__ = wdlang.__doc__

if hasattr(wdlang, "__all__"):
  __all__ = wdlang.__all__
