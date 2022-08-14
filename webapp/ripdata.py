#TIME
import time
from datetime import datetime 
import pytz 
#SOUP
from bs4 import BeautifulSoup 
import requests
#SQL
import sqlite3              
from sqlite3 import Error
import config
#DROP TABLE IF EXISTS employees;

#Pull
def pullWebsite(f,index):
    content=requests.get('https://www.kreuzgasse.de/neu/vplan/schueler/f{}/subst_00{}.htm'.format(f,index)).text
    log.append(logtimeprefix()+'pulled Website: .../f{}/00{}.htm'.format(f,index))
    return content

#Scraping
def getVabsOfScrap(f):
    soup=BeautifulSoup(pullWebsite(f,1),"html.parser")
    #<div class="mon_title">10.5.2022 Dienstag, Woche A (Seite 1 / 3)</div>
    found = soup.find("div","mon_title").string
    found = found.split()
    Datum,UploadTime,WochenTag,Weektyp=("",)*4
    arraylist=[]
    #arraylist= ['11.5.2022', 'Mittwoch', 'Woche', 'A', 'Seite', '1', '/', '2']
    for word in found:
        word=word.replace("(","")
        word=word.replace(")","")
        word=word.replace(",","")
        arraylist.append(word)        
    return arraylist

def createTables(Datum):
    #create manager
    try:
        c.execute("CREATE TABLE manager (Name_Datum text,AnzahlEinträge text,lastUpdate text,F integer,WochenTag text,WochenTyp text) ")
        log.append(logtimeprefix()+'created: table(manger)')
    except sqlite3.OperationalError:
        log.append(logtimeprefix()+'found: table(manager)')

    #create table/update table/manger   
    try:
        c.execute("CREATE TABLE '{}' (ID integer,Stunde text,Klasse text,Vertreter text,Lehrer text,Raum text,Fach text,Anmerkung text,Befund text) ".format(Datum))
        log.append(logtimeprefix()+'created: table({})'.format(Datum))
        shortlog.append(logtimeprefix()+'created: {}'.format(Datum))
        print(f"[ripdata] ==> Created '{Datum}'")
        return False
    except sqlite3.OperationalError:
        log.append(logtimeprefix()+'found: table({})'.format(Datum))
        c.execute("DROP TABLE '{}'".format(Datum))
        log.append(logtimeprefix()+'droped: table({})'.format(Datum))
        c.execute("CREATE TABLE '{}' (ID integer,Stunde text,Klasse text,Vertreter text,Lehrer text,Raum text,Fach text,Anmerkung text,Befund text) ".format(Datum))
        log.append(logtimeprefix()+'recreated: table({})'.format(Datum))
        shortlog.append(logtimeprefix()+'recreated: {}'.format(Datum))
        return True
        #log.append(logtimeprefix()+'updated: table(manager:{})'.format(kgDatum))
    
def fillTables(f):
    #Fill Variables
    arrayList=getVabsOfScrap(f)
    kgDatum=arrayList[0]
    kgTag=arrayList[1]
    kgWochenTyp=arrayList[3]
    try:kgSeiten=int(arrayList[7])
    except IndexError:kgSeiten=int('1')
    #print('Datum: '+kgDatum+' Tag: '+kgTag+' WochenTyp: '+kgWochenTyp+' Seiten: '+str(kgSeiten))

    #create Tables
    update=createTables(kgDatum)
    content=''
    for index in range(kgSeiten):
        content=content+pullWebsite(f,index+1)
    soup=BeautifulSoup(content,"html.parser")

    #Fill Variables Round 2 
    i,id,x = (0,)*3
    stunde,klasse,lehr1,lehr2,raum,fach,anmerkung = ("",)*7

    
    #Fill table
    for tag in soup.find_all("td","list"):
        #print(tag)
        #print(str(i)+". "+tag.string)
        if tag.string=='\xa0':
                tag.string=' '
        if(i==6):
            i=0
            anmerkung=tag.string
            typ='default'
            if lehr1=="+":
                if raum=="EVA":typ='EVA'
                elif raum=="---":typ='Entfall'
            elif lehr1==lehr2:
                if raum=="---":typ='Entfall'
                else: typ='Raum Vertretung => '+raum
            elif lehr2==' ':
                typ=anmerkung+' '+raum
            elif lehr1!=lehr2:
                typ='Vertretung '+lehr1+' '+raum
                
            c.execute("INSERT INTO '{}' VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(kgDatum,x,stunde,klasse,lehr1,lehr2,raum,fach,anmerkung,typ))
            x=x+1
        else:
            if i==0:stunde=tag.string
            if i==1:klasse=tag.string
            elif i==2:lehr1=tag.string
            elif i==3:lehr2=tag.string
            elif i==4:raum=tag.string
            elif i==5:fach=tag.string
            i=i+1
    log.append(logtimeprefix()+'filled: table({}) with f{}'.format(kgDatum,f))
    shortlog.append(logtimeprefix()+'f{}: filled: {}'.format(f,kgDatum))
    #Fill Variables Round 3 
    c.execute("SELECT Count(*) FROM '{}'".format(kgDatum))
    numberOfRows = c.fetchone()[0]
    
    #fill Tables
    if update==True:
        print(f"[ripdata] ==> Updated '{kgDatum}' ({numberOfRows})")
        #print(datetime.now(pytz.timezone('Europe/Berlin')).strftime("([%H:%M:%S] %d.%m.%Y) updated: "),kgDatum,kgTag,kgWochenTyp,numberOfRows)
        c.execute("UPDATE manager SET Name_Datum='{}',AnzahlEinträge='{}',lastUpdate='{}',F='{}',WochenTag='{}',WochenTyp='{}' WHERE Name_Datum='{}'".format(kgDatum,numberOfRows,'Updated last: '+currenttime,f,kgTag,kgWochenTyp,kgDatum))
        log.append(logtimeprefix()+'updated: table(manger/{}) with f{}'.format(kgDatum,f))
        shortlog.append(logtimeprefix()+'f{}: updated: manger'.format(f,kgDatum))
    else:
        c.execute("INSERT INTO manager VALUES ('{}','{}','{}','{}','{}','{}')".format(kgDatum,numberOfRows,'Updated last: '+currenttime,f,kgTag,kgWochenTyp))
        log.append(logtimeprefix()+'filled: table(manger/{}) with f{}'.format(kgDatum,f))
        shortlog.append(logtimeprefix()+'f{}: filled: manger'.format(f,kgDatum))


def logtimeprefix():
    time=datetime.now(pytz.timezone('Europe/Berlin')).strftime("[%H:%M:%S:%f")[:-3]
    time=time+"]: "
    return time

    ##Time Setup: currenttime##
currenttime=datetime.now(pytz.timezone('Europe/Berlin')).strftime("(%H:%M:%S) %d.%m.%Y ")
#print(currenttime)


def run():
  start_time = time.time()
  ####Setup####
  #LOG
  global log
  log=[]
  global shortlog
  shortlog=[]
  
  #Sqlite create/update tables
  connect=sqlite3.connect('webapp\data\Vertretungplan.db')
  global c
  c=connect.cursor()
  log.append(logtimeprefix()+'connection opend: daten , created cursor')
  fillTables(1)
  fillTables(2)
  connect.commit()
  connect.close()

  log.append(logtimeprefix()+'connection commited and closed')
  #LOG
  with open('log.txt', 'a') as f:
      f.write("-------["+currenttime+"]-------")
      f.write('\n')
      for index in log:
          f.write(index)
          f.write('\n')
      f.write('\n')
  with open('shortlog.txt', 'a') as f:
      f.write("-------["+currenttime+"]-------")
      f.write('\n')
      for index in shortlog:
          f.write(index)
          f.write('\n')
      f.write('\n')

  print(f"--- ripped data in {round(time.time() - start_time,3)} seconds --- waiting {config.ripdelay}s ---" )
