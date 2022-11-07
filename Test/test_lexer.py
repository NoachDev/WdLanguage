# import module to test
from wdlang.Parser import WdReader
import json

retRead = WdReader("../App_test/Pages/__init__.wd", {"__master__" : "main"})
# |
# var presets | wd componenets 
# var wd_vars | wd variables 
# var presets | wd comments 
# var presets | wd preset 

def test_varibels():
  vars_expct : dict = {
    "__master__"  : "main"  ,
    "df_bg"       : "gray23",
    "df_destac"   : "gray30",
    "df_desabl"   : "gray55",
    "df_fg"       : "white" ,
    "font_family" : "Caviar Dreams",
    "font_size"   : 10      ,
    "font"        : "(Caviar Dreams, 10)", # (font_family, font_size)
    # "font"        : ("font_family", "font_size")
  }

  assert vars_expct == retRead.wd_vars
  

def test_presets():
  prest_expct  = {
    "slim" : {
      "self" : {
        "bg" : "gray23" # df_bg
      }
    }
  }

  for preset, value in prest_expct.items():
    assert preset in retRead.presets

    for name, atrb in value["self"].items():
      assert retRead.presets[preset]["self"][name] == atrb 

  pass

def test_widgets():
  widg_expct : dict = {
    'main' : {
      'self': {'presets': 'slim'},
      'segments': {
        'atrb': [],
        'cmds': [{
          'title'           : {'args': 'Tk_test', 'kwargs': {}},
          'rowconfigure'    : {'args': 0, 'kwargs': {'weight': 1}},
          'columnconfigure' : {'args': 0, 'kwargs': {'weight': 1}}
          }]
        }
    },
    'f_test': {
      'self'    : {'tk_type': 'Frame', 'presets': 'slim'},
      'segments': {
        'atrb': [{'highlightthickness': 2, 'width': 30, 'height': 30}],
        'cmds': [{'place': {'args': [], 'kwargs': {'x': 100, 'y': 100}}}]
      }
    }
  }

  assert widg_expct == retRead.widgets

if __name__ == "__main__":
  # print(json.dumps(retRead, indent=2))
  print(json.dumps(retRead.wd_vars, indent=2))
  
  test_varibels()
  test_presets()
  test_widgets()

  pass
