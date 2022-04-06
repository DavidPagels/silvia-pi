#!/usr/bin/python

if __name__ == '__main__':
  import config as conf
  import asyncio
  import logging
  import pickle
  import sys
  from aiohttp import web
  from hardware import boiler, temperature_sensor
  from coroutines.HeatingElementController import HeatingElementController
  from coroutines.PidHandler import PidHandler
  from coroutines.RestServer import rest_server

  log = logging.getLogger("asyncio")
  logging.basicConfig(level=logging.DEBUG)
  set_point = pickle.load( open( sys.path[0] + "/setpoint.p", "rb" ) )["set_point"]

  loop = asyncio.get_event_loop()

  if conf.testing:
    boiler = boiler.EmulatedBoiler(conf.he_pin)
    temperature_sensor = temperature_sensor.EmulatedTemperatureSensor(boiler) # simulate temperature changes given boiler state
  else:
    boiler = boiler.Boiler(conf.he_pin)
    temperature_sensor = temperature_sensor.TemperatureSensor()

  pid_handler = PidHandler(log, temperature_sensor, conf.p, conf.i, conf.d, set_point, conf.sample_time)
  heating_element_controller = HeatingElementController(log, boiler, pid_handler)
  web_server = rest_server(log, conf.port, pid_handler, boiler)

  asyncio.ensure_future(pid_handler.pid_loop())
  asyncio.ensure_future(heating_element_controller.update_he_from_pid())
  asyncio.ensure_future(web.run_app(web_server), port = conf.port)
  try:
    loop.run_forever()
  finally:
    del boiler
