from crypt import methods
import json
from re import L
import secrets
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
from flaskext.mysql import MySQL
import psycopg2

app = Flask(__name__)
CORS(app)

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_PORT'] = 3306

# mysql = MySQL()
# mysql.init_app(app)
con = psycopg2.connect("dbname=postgres user=postgres host=localhost password=root port=54321")
con.autocommit = True
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/get")
def mainta():
    return "fine"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    uploaded = 'Successfully uploaded file into database'
    print(request.get_json())
    try:
        schema = request.form['schema']
        table = request.form['table']
        print(schema, table)
        print('req - -------    - ', request.files)
        app.config['MYSQL_DATABASE_DB'] = schema
        file = request.files['file']
        df = pd.read_excel(file, engine='openpyxl')
        df = df.fillna('')
        col = df.columns.values.tolist()
        print('---',type(col))
        print(col)
        print('-------------------')
        cursor = con.cursor()
        cursor.execute('select * from schemaone.tableone')
        print(cursor.fetchall())
        # cursor.execute("insert into schemaone.tableone (employee_id, site, payment_amount, hours, week_date) values ('2','asdf','34', '23', 'sdf')")
        # cursor = mysql.get_db().cursor()
        if table == 'tableone':
            for index, row in df.iterrows():
                cursor.execute("INSERT into"+schema+".tableone (employee_id, site, payment_amount, hours, week_date) values (%s, %s, %s, %s, %s)", (row[col[0]], row[col[1]], row[col[2]], row[col[3]], row[col[4]]))
        elif table == 'tabletwo':
            for index, row in df.iterrows():
                cursor.execute("INSERT into "+schema+".tabletwo (post_date, site, versions, job_level, comment, emotions, response, category, sla, status, likes, dislikes, vote) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[col[0]], row[col[1]], row[col[2]], row[col[3]], row[col[4]], row[col[5]], row[col[6]], row[col[7]], row[col[8]], row[col[9]], row[col[10]], row[col[11]], row[col[12]]))
        print(cursor)
        cursor.close()
        print(file)
    except Exception as e:
        print('error')
        uploaded = 'Error in uploading file into database'
        print(e)

    response = jsonify({"statusCode": 200, "body": {"message": uploaded}})
    return response


if __name__ == "__main__":
    app.run()
