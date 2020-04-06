from flask import Flask, render_template,redirect,request
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
import json

app = Flask(__name__)

@app.route('/')
def index(fireToast='-1'):
    cursor.execute('SELECT * from '+currentTable+' ')
    return render_template('index.html',todos=cursor.fetchall(),fireToast=fireToast)

@app.route('/todos/',methods=['GET','POST'])
def showTodos(check='0'):
    cursor.execute('SELECT * FROM tableNames')
    temp = cursor.fetchall()
    return render_template('todos.html',tableNames = temp,check=check)

@app.route('/add/',methods=['GET','POST'])
def handleHomePost():
    if request.method=='POST':
        todo = request.form['todo']
        cursor.execute("INSERT INTO "+currentTable+" VALUES(?)",(todo))
        cursor.commit()        
    return index(fireToast='1')

@app.route('/update/',methods=['GET','POST'])
def handleUpdate():
    if request.method=='POST':
        todoID,message= request.form['updateID'].split(',')

        cursor.execute("update "+currentTable+" set todo = ? where todoID = ?",(message,int(todoID)))
        cursor.commit()        
    return index(fireToast='1')

@app.route('/delete/',methods=['GET','POST'])
def handleDelete():
    
    if request.method == 'POST':
        id = request.form['deleteID']
        try:
            int(id)
        except:
            return index(fireToast='0')
        else:    
           
            cursor.execute("Delete From "+currentTable+" where todoID = ?",(int(id)))
            cursor.commit()
            cursor.execute("SELECT "+currentTable+".todo from "+currentTable+" where todoID>?",(int(id)))
            tempTodos = cursor.fetchall()
            cursor.execute("DELETE from "+currentTable+" where todoID>?",(int(id)))
            cursor.execute("DBCC CHECKIDENT ( "+currentTable+" , RESEED, ?) ",(int(id)-1))
            for todo in tempTodos:
                cursor.execute("INSERT INTO "+currentTable+" VALUES(?)",(todo))
            cursor.commit()            
            return index(fireToast='1')

@app.route('/addTodoList/',methods=['GET','POST'])
def handleAddTodoList():
    global currentTable
    currentTable = str(request.form['tableName'])
    cursor.execute("""CREATE TABLE """+currentTable+""" (
        todoID INT NOT NULL PRIMARY KEY IDENTITY,
        todo TEXT
    ) """) 
    cursor.execute('INSERT INTO tableNames VALUES(?)',currentTable)
    return redirect('/')

@app.route('/showList/',methods=['GET','POST'])
def handleShowList():
    global currentTable
    currentTable = request.form['tableName']
    return redirect('/')

@app.route('/dropList/',methods=['GET','POST'])
def handelDropList():
    listName = request.form['listName']
    if currentTable==listName :
        return showTodos(check=1)
    else:
        try:
            cursor.execute('DROP TABLE  '+listName)   
        except:
            return redirect('/todos/')
        else:   
            cursor.execute('DELETE FROM tableNames where CAST(name as VARCHAR(128)) = CAST( ? as VARCHAR(128))',listName) 
            cursor.commit()
            return redirect('/todos/')



@app.errorhandler(404) 
def invalid_route(e):
    return render_template('404.html')





if __name__ =='__main__':
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=NameerPC\MSSQL;'
                        'Database=tempDB;'
                        'Trusted_Connection=yes;')
    conn.autocommit = True
    cursor = conn.cursor()
    # cursor.execute('CREATE DATABASE TodosDB')
    cursor.execute('USE TodosDB')
    try:
         cursor.execute('''CREATE TABLE baseList(
            todoID INT NOT NULL PRIMARY KEY IDENTITY,
            todo TEXT
            )''')
         cursor.execute('''CREATE TABLE tableNames(
            tableID INT NOT NULL PRIMARY KEY IDENTITY,
            name TEXT
            ) ''')
    except:
        cursor.execute("SELECT tableNames.name from tableNames Where CAST(name as VARCHAR(128)) = 'baseList' ")
        holdResponse = cursor.fetchall()
        if len(holdResponse) == 0:
            cursor.execute("INSERT INTO tableNames VALUES('baseList')")
        # True
    finally:
    # cursor.execute("INSERT INTO tableNames VALUES('baseList')")
        currentTable="baseList"
        app.run(debug=True)
