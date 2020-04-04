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

@app.route('/update/')
def handleUpdate():
    return redirect('/')

@app.route('/delete/')
def handleDelete():
   return redirect('/')
if __name__ =='__main__':    app.run(debug=True)
