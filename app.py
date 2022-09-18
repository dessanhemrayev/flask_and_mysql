from flask import Flask, render_template, request, redirect, url_for, session,Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sqlite3

from export_excel import excel_file

app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'wtuser'
 
 
mysql = MySQL(app)
 
 
                            # @app.route('/')
@app.route('/login', methods =['POST'])
def login():
    msg = ''
    print(request.form)
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form:
        if request.form.get('action1'):                                                # 1 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('SELECT * FROM product')
        # result = cursor.fetchone() # fetchone() выводит одну строчку
            result = cursor.fetchall() #   в
            print(result)
            if result:
                keys=list(result[0].keys())
                print(keys)
            # session['loggedin'] = True
            # session['id'] = result['id']
            # session['fname'] = result['login']
                msg = 'Logged in successfully !'
                return render_template('qwe.html', msg = result,keys=keys)


        if request.form.get('action2'):                                             #  2 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('SELECT id, name FROM product WHERE name = % s ', (fname,))
            result = cursor.fetchall() 
            print(result)
            if result:
                keys=list(result[0].keys())
                output = excel_file(keys,result)
                filename = 'otchet'
                return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":f"attachment;filename={filename}.xls"})

                # return render_template('qwe.html', msg = result,keys=keys)

                
        if request.form.get('action3'):                                             #  3 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('DELETE FROM product WHERE name = % s ', (fname,))
           # result = cursor.fetchall() 
            print('удаление выполнено')
            # if result:
            #     keys=list(result[0].keys())
            #     print(keys)
            #     msg = 'Logged in successfully !'
            #     return render_template('qwe.html', msg = result,keys=keys)
       
    else:
        msg = 'Incorrect fname / lname !'
    return render_template('qwe.html', msg = msg)

# @app.route('/users', methods =['POST'])
# def users():
#     msg = ''
#     print(request.form)
#     if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form:
        
#         fname = request.form['fname']
#         lname = request.form['lname']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
#         cursor.execute('SELECT * FROM product where ')
        
#         result = cursor.fetchall() # результат запроса 
#         print(result)
#         if result:
#             keys=list(result[0].keys())
#             print(keys)
            
#             msg = 'Logged in successfully !'
#             return render_template('qwe.html', msg = result,keys=keys)
        
#         else:
#             msg = 'Incorrect fname / lname !'
#     return render_template('qwe.html', msg = msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port="8888")

    