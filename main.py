from webapp import createblank
from webapp import ripdata
import time
import config 

while True:
  ripdata.run()
  time.sleep(config.ripdelay)