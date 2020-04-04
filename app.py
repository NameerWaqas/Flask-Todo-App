from flask import Flask, render_template,redirect,request
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
app = Flask(__name__)

@app.route('/')
def index():
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

    return render_template('index.html',todos=cursor.fetchall())
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
    return redirect('/')

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
    return redirect('/')

@app.route('/delete/',methods=['GET','POST'])
def handleDelete():
    if request.method == 'POST':
        id = request.form['deleteID']
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=NameerPC\MSSQL;'
                      'Database=tempDB;'
                      'Trusted_Connection=yes;')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("Delete From todoTable where todoID = ?",(int(id)))
        cursor.commit()
        cursor.execute("select COUNT(todoID) from todoTable")
        maxID = cursor.fetchall()
        cursor.execute("DBCC CHECKIDENT ('todoTable', RESEED, ?) ",(int(maxID[0][0])))
        cursor.commit()        
    return redirect('/')



if __name__ =='__main__':    app.run(debug=True)
