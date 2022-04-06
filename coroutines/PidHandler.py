import PID as PID
import asyncio
import logging
from collections import deque
from time import time
import csv
from datetime import datetime

class PidHandler:
  i=0
  pidhist = deque([0.]*10)
  avg_pid = 0.
  temphist = deque([0.]*5)
  avg_temp = 0.
  lasttime = time()

  def __init__(self, log, temperature_sensor, p, i, d, set_point, sample_time):
    self.log = log
    self.temperature_sensor = temperature_sensor
    self.pid = PID.PID(p, i, d)
    self.pid.SetPoint = set_point
    self.pid.setSampleTime(sample_time * 5)
    self.set_point = set_point
    self.sample_time = sample_time

  def set_set_point(self, set_point):
    import pickle, sys

    self.pid.SetPoint = set_point
    self.set_point = set_point
    pickle.dump({"set_point": set_point}, open(str(sys.path[0]) + "/setpoint.p", "wb" ))

  async def pid_loop(self):
    with open("Failedcsv.csv","a+") as tempFile:
      fieldNames = ["time","avgtemp","settemp"]
      writer = csv.DictWriter(tempFile,fieldnames=fieldNames)
 
      while True:
        try:
          temp = self.temperature_sensor.get_temperature()
        except:
          continue

        self.temphist.popleft()
        self.temphist.append(temp)
        self.avg_temp = sum(self.temphist) / len(self.temphist)

        if self.i % 10 == 0 :
          self.pid.update(self.avg_temp)
          self.pidout = self.pid.output
          self.pidhist.popleft()
          self.pidhist.append(self.pidout)
          self.avg_pid = sum(self.pidhist) / len(self.pidhist)
          writer.writerow({"time": datetime.now(), "avgtemp":self.avg_temp,"settemp":self.set_point})

        sleeptime = self.lasttime + self.sample_time - time()
        if sleeptime < 0 :
          sleeptime = 0
        await asyncio.sleep(sleeptime)
        self.i += 1
        self.lasttime = time()

