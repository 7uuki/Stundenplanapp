tage = ["Montag","Dienstag","Mitwoch","Donnerstag","Freitag"]
blöcke = [
    dict(
        start="8:30",
        end="10:00",
        text="1.Block (1-2)",
        block=1,
    ),
    dict(
        start="10:20",
        end="11:15",
        text="2.Block (3-4)",
        block=2,
    ),
    dict(
        start="12:15",
        end="13:45",
        text="3.Block (5-6)",
        block=3,
    ),
    dict(
        start="14:00",
        end="15:30",
        text="4.Block (7-8)",
        block=4,
    ),
    dict(
        start="15:35",
        end="17:05",
        text="5.Block (9-10)",
        block=5,
    ),
]


#makes string for creating a table CREATE TABLE blöcke (Anfang text,Ende text,id text)
shema=dict(
    blöcke = dict(
        Anfang="text",
        Ende="text",
        text="text",
        id="text",
    ),
    plan = dict(
        Tag="text",
        Fach="text",
        Woche="text",
        Block="text",
        Raum="text",
        Anfang="text",
        Ende="text",
    ),
    fächer = dict(
        Fach="text",
        Art="text",
        Lehrer="text",
    ),
    tage = dict(
        Tag="text",
    ),

)

def table_create(table):
    string=''
    if shema[table]!='{}':
        for i in shema[table]:
            string+=i+" "+shema[table].get(i)+","    
    else:
        string=","
    return f"CREATE TABLE {table}({string[:-1]})"
