from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sqlite3

from export_excel import generate_excel_file

app = Flask(__name__)


app.secret_key = "your secret key"


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "to-do"


mysql = MySQL(app)


@app.route("/login", methods=["POST"])
def login():
    msg = ""
    if request.method == "POST" and "fname" in request.form and "lname" in request.form:
        if request.form.get("action1"):  # 1 кнопка
            fname = request.form["fname"]
            lname = request.form["lname"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM user")
            result = cursor.fetchall()  #   в
            if result:
                keys = list(result[0].keys())
                msg = "Logged in successfully !"
                data = {"user_name": fname, "project_name": lname}
                return render_template("project.html", msg=result, keys=keys, data=data)

        if request.form.get("action2"):  #  2 кнопка
            fname = request.form["fname"]
            lname = request.form["lname"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT id, login FROM user WHERE login = % s ", (fname,))
            result = cursor.fetchall()
            if result:
                keys = list(result[0].keys())
                data = {"user_name": fname, "project_name": lname}
                return render_template("project.html", msg=result, keys=keys, data=data)

        if request.form.get("action3"):  #  3 кнопка
            fname = request.form["fname"]
            lname = request.form["lname"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM user WHERE login = % s ", (fname,))
            mysql.connection.commit()
            cursor.close()

        if request.form.get("action4"):  #  4 кнопка
            fname = request.form["fname"]
            lname = request.form["lname"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO user (login, email,parol)  VALUES ("коля", "апв","1235");'
            )

            mysql.connection.commit()
            cursor.close()

    else:
        msg = "Incorrect fname / lname !"
    return render_template("project.html", msg=msg)


@app.route("/export", methods=["POST"])
def export():
    if request.form.get("action5"):
        fname = request.form["fname"]
        lname = request.form["lname"]  #  5 кнопка
        control = "*"
        if lname != "type" or fname != "type":
            control = "id,login"

        query = f"SELECT {control} FROM user"
        fields = ["fname", "lname"]
        hash_fields = {"fname": "login", "lname": "id"}
        add_query = []
        add_query_value = []
        for item in fields:
            if request.form[item] != "type":
                add_query.append(f"{hash_fields[item]} = % s")
                add_query_value.append(request.form[item])
        if len(add_query):
            query += " WHERE " + " or ".join(add_query)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, tuple(add_query_value))
        result = cursor.fetchall()
        if result:
            keys = list(result[0].keys())
            output = generate_excel_file(
                keys, result
            )  # формирование файла для скачивания
            filename = "otchet"
            return Response(
                output,
                mimetype="application/ms-excel",
                headers={"Content-Disposition": f"attachment;filename={filename}.xls"},
            )


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port="8888")
