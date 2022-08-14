import sqlite3              
from sqlite3 import Error
import config
def create():
  connect=sqlite3.connect('Stundenplan.db')
  global c
  c=connect.cursor()
  a = config.blöcke[1]
  try:
    c.execute(config.table_create("blöcke"))
    for i in config.blöcke:
      c.execute("INSERT INTO blöcke VALUES ('{}','{}','{}','{}')".format(i.get('start'),i.get('end'),i.get('text'),i.get('block')))

    c.execute(config.table_create("tage"))
    for i in config.tage:
      c.execute("INSERT INTO tage VALUES ('{}')".format(i))
    
    c.execute(config.table_create("fächer"))
    c.execute("INSERT INTO fächer VALUES ('{}','{}','{}')".format("wähle ein fach","unbekannt","unbekannt"))
    c.execute(config.table_create("plan"))
    connect.commit()
    connect.close()
  except sqlite3.OperationalError:
    return

create()
