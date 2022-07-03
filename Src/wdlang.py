#!/bin/python3

from tkinter import *
from tkwd import Constuct
from pathlib import Path

import argparse, os

class App(Tk):
  def __init__(self, Pages, Functions):
    super().__init__()

    Constuct(".", self, Pages, Functions)

    self.mainloop()

parser = argparse.ArgumentParser()
parser.add_argument("-sd", '--Src_Directory', help="use to set Main Path of have folder Pages and Funtions")
parser.add_argument("-sf", '--Src_Functions', help="use to set folder Funtions")
parser.add_argument("-sp", '--Src_Pages'    , help="use to set folder Pages")

args = parser.parse_args()
Pages, Functions, main_path = None, None, None

if args.Src_Functions:
  Pages     : Path = Path(args.Src_Functions)

if args.Src_Pages:
  Functions : Path = Path(args.Src_Pages)

if args.Src_Directory:
  main_path : Path  = Path(args.Src_Directory)

if not Pages and not Functions:
  if not main_path:
    main_path = Path(os.getcwd())

  Functions : Path  = main_path.joinpath("Functions") 
  Pages     : Path  = main_path.joinpath("Pages")

if not Pages.exists():
  raise ValueError(Pages, main_path)

elif not Functions.exists():
  raise ValueError(Functions, main_path)

App(Pages, Functions)
