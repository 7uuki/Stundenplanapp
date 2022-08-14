from tkinter import *
import sqlite3              

def show_entry_fields():
   connect=sqlite3.connect(r'D:\Programming\Stundenplanapp\webapp\data\Stundenplan.db')
   global c
   c=connect.cursor()
   c.execute("INSERT INTO plan VALUES ('{}','{}','{}','{}')".format(e1.get(),e2.get(),e3.get(),e4.get()))
   e1.delete(0,END)
   e2.delete(0,END)
   e3.delete(0,END)
   e4.delete(0,END)
   e1.insert(0,"Montag")
   e3.insert(0,"A")
   connect.commit()
   connect.close()

master = Tk()
Label(master, text="Tag").grid(row=0)
Label(master, text="Fach").grid(row=2)
Label(master, text="Woche").grid(row=1)
Label(master, text="Block").grid(row=3)

e1 = Entry(master)
e1.grid(row=0, column=1)
e2 = Entry(master)
e2.grid(row=2, column=1)
e3 = Entry(master)
e3.grid(row=1, column=1)
e4 = Entry(master)
e4.grid(row=3, column=1)

Button(master, text='Quit', command=master.quit).grid(row=5, column=0, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=5, column=1, sticky=W, pady=4)

e1.insert(0,"Montag")
e3.insert(0,"A")

mainloop( )