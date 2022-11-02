import time

class Long_press:
  def __init__(self, widget, long_function, small_function, ms_time_press : float = 300):
    self.widget, self.long_function, self.small_function, self.ms_time_press = widget, long_function, small_function, ms_time_press

    self.time_clock : int = 0
    
  def app_event(self, event : str, type_event : str = ""):
    self.widget.bind(f"<{type_event}Release-{event}>", self._release_)
    self.widget.bind(f"<{type_event}-{event}>"       , self._press_)

  def _release_(self, Event):
    ttime = (time.time() - self.time_clock) * 1000

    if ttime >= self.ms_time_press:
      self._long_   : bool = False

      if callable(self.long_function):
        self.long_function(Event)

    else:
      if callable(self.small_function):
        self.small_function(Event)
      
  def _press_(self, Event):
    self.time_clock = time.time()
  
class Event_Load:
  def __init__(self, button_events : dict = {}, key_events : dict = {}):
    self.key_events       : dict = key_events
    self.button_events    : dict = button_events

    self.key_function     : dict = {}
    self.button_function  : dict = {}

    self.event_type       : dict = {"buttons" : self.button_events, "keys" : self.key_events}

  def append_button_events(self, events_app : dict):
    if type(events_app) == dict:
      self.test_outscope = True
      self.button_events = {**self.button_events, **events_app}
      self.event_type["buttons"] = self.button_events

  def append_key_events(self, events_app : dict):
    if type(events_app) == dict:
      self.key_events = {**self.key_events, **events_app}
      self.event_type["keys"] = self.key_events

  def __binds__(self, widget, src : dict, add : dict, compl : str = "") -> None:
    
    for type_event, function in src.items():
      
      if function == "push":
        function = None
      
      if type(type_event) == tuple:
        type_, event_ = type_event

      else:
        type_, event_ = "small", type_event

      if type_ == "long":
        _long_  = function
        _small_ = None
        
      else:
        _long_  = None 
        _small_ = function

      if not widget in add:
        add[widget] = {}

      if event_ in add[widget]:
        _function_ : Long_press     = add[widget][event_]

        if _long_:
          _function_.long_function  = _long_

        elif _small_:
          _function_.small_function = _small_

      else:

        _function_  = Long_press(widget, _long_, _small_)
        _function_.app_event(event_, compl)

        add[widget][event_] = _function_

  def Run_button_binds(self, widget):
    self.__binds__(widget, self.button_events, self.button_function, "Button")

  def Run_key_binds(self, widget):
    self.__binds__(widget, self.key_events, self.key_function, "Key")

  def Run_binds(self, widget):
    self.Run_button_binds(widget)
    self.Run_key_binds(widget)

  def del_button_binds(self, widget):
    self.button_function.pop(widget)

  def del_key_binds(self, widget):
    self.key_function.pop(widget)
  
  def del_binds(self, widget):
    self.del_button_binds(widget)
    self.del_key_binds(widget)
  
  def __str__(self) -> str:
    str_ret = "Buttons\n"

    for k , v in self.event_type["buttons"].items():
      str_ret += "\t" + str(v) + "\n"

      str_ret += "\t\t type : " + str(k[0]) + "\n"
      str_ret += "\t\t call : " + str(k[1]) + "\n"
    
    str_ret += "Keys\n"

    for k , v in self.event_type["keys"].items():
      str_ret += "\t" + str(v) + "\n"

      str_ret += "\t\t type : " + str(k[0]) + "\n"
      str_ret += "\t\t call : " + str(k[1]) + "\n"

    str_ret += "-" * 15 + "\n"
    
    return str_ret + str(__class__)
  
    