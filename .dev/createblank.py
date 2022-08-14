import sqlite3              
from sqlite3 import Error
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
import config
  

def create():
  connect=sqlite3.connect(sys.path[0]+'\webapp\data\Stundenplan.db')
  global c
  c=connect.cursor()
  a = config.blöcke[1]
  try:
    c.execute(table_create("blöcke",config))
    for i in config.blöcke:
      c.execute("INSERT INTO blöcke VALUES ('{}','{}','{}','{}')".format(i.get('start'),i.get('end'),i.get('text'),i.get('block')))

    c.execute(table_create("tage",config))
    for i in config.days:
      c.execute("INSERT INTO tage VALUES ('{}')".format(i))
    
    c.execute(table_create("fächer",config))
    c.execute("INSERT INTO fächer VALUES ('{}','{}','{}')".format("wähle ein fach","unbekannt","unbekannt"))
    c.execute(table_create("plan",config))
    connect.commit()
    connect.close()
    print("blank Stundenplan.db created")
  except sqlite3.OperationalError:
    return

def table_create(table,config):
    string=''
    shema=config.shema
    if shema[table]!='{}':
        for i in shema[table]:
            string+=i+" "+shema[table].get(i)+","    
    else:
        string=","
    return f"CREATE TABLE {table}({string[:-1]})"

create()
