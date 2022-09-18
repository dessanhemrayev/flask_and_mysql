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
app.config['MYSQL_DB'] = 'to-do'
 
 
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
            cursor.execute('SELECT * FROM user')
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
                data={'user_name':fname,'project_name':lname}
                return render_template('qwe.html', msg = result,keys=keys,data=data)


        if request.form.get('action2'):                                             #  2 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('SELECT id, login FROM user WHERE login = % s ', (fname,))
            result = cursor.fetchall() 
            print(result)
            if result:
                keys=list(result[0].keys())
                data={'user_name':fname,'project_name':lname}
                return render_template('qwe.html', msg = result,keys=keys,data=data)

    
                
        if request.form.get('action3'):                                             #  3 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('DELETE FROM user WHERE login = % s ', (fname,))   
            print('удаление выполнено')
            mysql.connection.commit() 
            cursor.close()
            # if result:
            #     keys=list(result[0].keys())
            #     print(keys)
            #     msg = 'Logged in successfully !'
            #     return render_template('qwe.html', msg = result,keys=keys)
        
        if request.form.get('action4'):                                             #  4 кнопка
            fname = request.form['fname']
            lname = request.form['lname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
            cursor.execute('INSERT INTO user (login, email,parol)  VALUES ("коля", "апв","1235");')
         
            print('запись добавлена')
            mysql.connection.commit()
            cursor.close()
    
    else:
        msg = 'Incorrect fname / lname !'
    return render_template('qwe.html', msg = msg)


@app.route('/export', methods =['POST'])
def export():

    if request.form.get('action5'): 
        fname = request.form['fname']
        lname = request.form['lname']                                            #  5 кнопка
        control='*'
        if lname!='type' or fname!='type':
            control='id,login'

        query = f'SELECT {control} FROM user'
        fields = ['fname','lname']
        hash_fields = {'fname':'login','lname':'id'}
        add_query = []
        add_query_value = []
        for item in fields:
            if request.form[item]!='type':
                add_query.append(f"{hash_fields[item]} = % s")
                add_query_value.append(request.form[item])  
        if len(add_query):
            query += ' WHERE '+' or '.join(add_query)
        print(query)
        print(add_query_value)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM user WHERE login = % s ', (fname,))
        cursor.execute(query, tuple(add_query_value))
        result = cursor.fetchall() 
        print(result)
        if result:
            keys=list(result[0].keys())
            output = excel_file(keys,result)  #формирование файла для скачивания 
            print(output) 
            filename = 'otchet'
            
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":f"attachment;filename={filename}.xls"},)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port="8888")

    