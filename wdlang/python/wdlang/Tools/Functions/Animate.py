import threading, time
from math import sqrt, sin, cos, atan, degrees, radians, pi

class __calcule__:
  def __init__(self, ptx_start : int, pty_start : int, ptx_end : int, pty_end : int, propotion : int):
    self.range_x = [ptx_start]
    self.range_y = [pty_start]

    if pty_start != pty_end and ptx_start != ptx_end:
      self.ox = ptx_start
      self.oy = pty_start

      if ptx_start > ptx_end:
        self.ox = -ptx_start

      if pty_start > pty_end:
        self.oy = -pty_start

      self.dx = ptx_end - ptx_start
      self.dy = pty_end - pty_start

      tangt = sqrt(self.dx**2 + self.dy**2)
      angle = degrees(atan(abs(self.dx / self.dy)))

      for t in range(int(tangt)):
        self.range_y.append(sqrt((t * cos(angle * (pi/180)) + self.oy)**2))
        self.range_x.append(sqrt((t * sin(radians(angle)) + self.ox)**2))
    else:
      if pty_start != pty_end:

        if pty_start > pty_end:
          self.range_y.extend(list(range(pty_end, pty_start))[::-1])
        else:
          self.range_y.extend(list(range(pty_start, pty_end)))

      if ptx_start != ptx_end:
        if ptx_start > ptx_end:
          self.range_x.extend(list(range(ptx_end, ptx_start))[::-1])
        else:
          self.range_x.extend(list(range(ptx_start, ptx_end)))

      self.dxy = len(self.range_x) - len(self.range_y)

      if self.dxy > 0:
        self.range_y += [pty_end] * self.dxy

      elif self.dxy < 0:
        self.range_x += [ptx_end] * self.dxy

    self.range_x = self.range_x[::propotion]
    self.range_y = self.range_y[::propotion]

    self.range_x.append(ptx_end)
    self.range_y.append(pty_end)

class Motion(__calcule__):
  def __init__(self, widget, ptx_end : int, pty_end : int, propotion : int, stime_slp : float = 0.1):
    self.widget = widget
    self.stime_slp = stime_slp

    self.place_i = self.widget.place_info()

    if int(self.place_i["relx"]) > 0:
      x = self.widget.master.winfo_reqwidth()
      x = (int(self.place_i["relx"]) * 100) * x /100

    else:
      x = int(self.place_i["x"])

    if int(self.place_i["rely"]) > 0:
      y = self.widget.master.winfo_reqheight()
      y = (int(self.place_i["rely"]) * 100) * x /100

    else:
      y = int(self.place_i["y"])
    
    print(x, y)
    super().__init__(x, y, ptx_end, pty_end, propotion)

    threading.Thread(target=self.move).start()  

  def move(self):
    try:
      for x, y in zip(self.range_x, self.range_y):
        self.widget.place(anchor = self.place_i["anchor"], x = x, y = y)
        time.sleep(self.stime_slp)
    except:
      pass

class Size(__calcule__):
  def __init__(self, widget, ptx_start : int, pty_start, ptx_end : int, pty_end : int, propotion : int, stime_slp : float = 0.1, onend= None):
    self.widget = widget
    self.stime_slp = stime_slp
    self.onend  = onend

    super().__init__(ptx_start, pty_start, ptx_end, pty_end, propotion)

    self.do = threading.Thread(target=self.size).start()  

  def size(self):
    try:
      for w, h in zip(self.range_x, self.range_y):
        self.widget.configure(width = w, height = h)
        time.sleep(self.stime_slp)
      
      if self.onend:
        self.onend()
        
    except:
      pass

    self.widget.update()