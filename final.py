import pymysql
import csv
import requests
from bs4 import BeautifulSoup
import pandas
from tkinter import *

root = Tk()
root.title("user input")
root.geometry("640x640")

heading = Label(root, text="WELCOME TO GOOGLE SCHOLAR DATABASE", font=('arail',20,'bold'), fg='steelblue').pack()
heading1 = Label(root, text="ENTER THE NUMBER", font=('arail',20,'bold'), fg='steelblue').place(x=10, y=120)

number = IntVar()
entry = Entry(root, textvariable=number, width=45, bg='steelblue').place(x=320, y=130)

work = Button(root, text='Enter', width=30, height=5, bg='lightblue').place(x=270, y=300)

root.mainloop()

a = pandas.read_excel('url.xlsx','Sheet1')

url=(a['URL'][number.get()])
response=requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find('tbody', attrs={'id': 'gsc_a_b'})

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll(['td','div']):
        text = cell.text.replace('&nbsp;', '')    
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)


db = pymysql.connect("localhost","AMS","abhay1972","scholar")

cursor = db.cursor()

sql = """CREATE TABLE PAPER37 (
         {} INT(4) AUTO_INCREMENT PRIMARY KEY,
         {} VARCHAR(255) ,
         {} VARCHAR(255) ,
         {} VARCHAR(255) ,
         {} INT(4),
         {} INT(4)  )""".format('SLNO','TITLE','AUTHOR','JOURNAL','CITATIONS','YEAR')

with open('test1.csv','w+',newline='') as fp:
    a = csv.writer(fp,delimiter=',')
    a.writerows(list_of_rows)


delete = "TRUNCATE PAPER37"

cursor.execute(delete)

rows=''
for i in range(len(list_of_rows)):
    if(list_of_rows[i][3]==''):
        list_of_rows[i][3]='0'
    if(list_of_rows[i][4]==''):
        list_of_rows[i][4]='0'
    if(list_of_rows[i][2]==''):
        list_of_rows[i][2]='N\A'
    rows = "('{}','{}','{}','{}','{}','{}')".format(i,list_of_rows[i][0],list_of_rows[i][1],list_of_rows[i][2],list_of_rows[i][3],list_of_rows[i][4])
    query = "INSERT INTO PAPER37 VALUES" + rows

    print(query)

    try:
          cursor.execute(query)
          db.commit()
    except:
          db.rollback()





    

