#from bottle import route, run, get, post, request, static_file, abort
from aiohttp import web
from subprocess import call
import os
import logging

async def rest_server(log, port, pidHandler, boiler):
  routes = web.RouteTableDef()

  @routes.route('*', '/')
  def docroot(request):
    return web.FileResponse(wwwdir + '/index.html')

  @routes.route('*', '/curtemp')
  def curtemp(request):
    return web.Response(text=str(pidHandler.avg_temp))

  @routes.get('/settemp')
  def settemp(request):
    return web.Response(text=str(pidHandler.set_point))

  @routes.post('/settemp')
  async def post_settemp(request):
    try:
      data = await request.post()
      settemp = float(data['settemp'])
      if settemp >= 40 and settemp <= 160 :
        pidHandler.set_set_point(settemp)
        return web.Response(text=str(settemp))
      else:
        return web.HTTPBadRequest(reason = 'Set temp out of range 40-160.')
    except:
      raise web.HTTPBadRequest(reason = 'Invalid number for set temp.')

  @routes.get('/allstats')
  def allstats(request):
    pid = pidHandler.pid
    response = {
      "i": pidHandler.i,
      "hestat": 1 if boiler.last_mode else 0,
      "settemp": pidHandler.set_point,
      "pterm": round(pid.Kp, 2),
      "iterm": round(pid.Ki, 2),
      "dterm": round(pid.Kd, 2),
      "pidval": round(pidHandler.pid.output),
      "avgpid": round(pidHandler.avg_pid, 2),
      "temp": pidHandler.temperature_sensor.get_temperature()
    }
    return web.json_response(response)

  @routes.route('*', '/restart')
  def restart(request):
    call(["reboot"])
    return '';

  @routes.route('*', '/shutdown')
  def shutdown(request):
    call(["shutdown","-h","now"])
    return '';

  @routes.get('/healthcheck')
  def healthcheck(request):
    return 'OK'



  basedir = os.path.dirname(os.path.realpath(__file__))
  wwwdir = basedir + '/../www/'
  log.info("wwwdir: " +  str(wwwdir))
  log.info("running the server now...")
  app = web.Application()
  routes.static('/', wwwdir)
  app.add_routes(routes)
  return app