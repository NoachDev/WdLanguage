from setuptools import setup

setup(
  name = "wdlang",
  version= "1.0.0",
  packages=["wdlang", "wdlang/Tools"],
  package_dir={"wdlang" : "wdlang"},
  entry_points={
    "console_scripts" : ["wdlang=wdlang:main"]
    },
  
)