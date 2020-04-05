from flask import Flask, render_template,redirect,request
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
app = Flask(__name__)

@app.route('/')
def index(fireToast='-1'):
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=NameerPC\MSSQL;'
                      'Database=tempDB;'
                      'Trusted_Connection=yes;')
    conn.autocommit = True
    cursor = conn.cursor()
    # cursor.execute('DROP TABLE todoTable')
    # cursor.execute('''CREATE TABLE todoTable(
    #     todoID INT NOT NULL PRIMARY KEY IDENTITY,
    #     todo TEXT
    # ) ''')
    cursor.execute('SELECT * from todoTable')
    return render_template('index.html',todos=cursor.fetchall(),fireToast=fireToast)

@app.route('/todos/',methods=['GET','POST'])
def showTodos():
    return render_template('todos.html')

@app.route('/add/',methods=['GET','POST'])
def handleHomePost():
    if request.method=='POST':
        todo = request.form['todo']
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=NameerPC\MSSQL;'
                      'Database=tempDB;'
                      'Trusted_Connection=yes;')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todoTable VALUES(?)",todo)
        cursor.commit()        
    return index(fireToast='1')

@app.route('/update/',methods=['GET','POST'])
def handleUpdate():
    if request.method=='POST':
        todoID,message= request.form['updateID'].split(',')
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=NameerPC\MSSQL;'
                      'Database=tempDB;'
                      'Trusted_Connection=yes;')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("update todoTable set todo = ? where todoID = ?",(message,int(todoID)))
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
            conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=NameerPC\MSSQL;'
                        'Database=tempDB;'
                        'Trusted_Connection=yes;')
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("Delete From todoTable where todoID = ?",(int(id)))
            cursor.commit()
            cursor.execute("SELECT todoTable.todo from todoTable where todoID>?",(int(id)))
            tempTodos = cursor.fetchall()
            cursor.execute("DELETE from todoTable where todoID>?",(int(id)))
            # cursor.execute("select COUNT(todoID) from todoTable")
            # maxID = cursor.fetchall()
            cursor.execute("DBCC CHECKIDENT ('todoTable', RESEED, ?) ",(int(id)-1))
            for todo in tempTodos:
                cursor.execute("INSERT INTO todoTable VALUES(?)",todo)
            cursor.commit()            
            return index(fireToast='1')

@app.route('/addTodoList',methods=['GET','POST'])
def handleAddTodoList():
    return render_template('index.html')

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')





if __name__ =='__main__':    app.run(debug=True)
