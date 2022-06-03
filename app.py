from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import psycopg2

app = Flask(__name__)
CORS(app)

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_PORT'] = 3306

# mysql = MySQL()
# mysql.init_app(app)
con = psycopg2.connect(dbname="postgres", user="postgres",  host="127.0.0.1", password="postgres", port="5432")
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
        # app.config['MYSQL_DATABASE_DB'] = schema
        file = request.files['file']
        df = pd.read_excel(file, engine='openpyxl')
        df = df.fillna('')
        col = df.columns.values.tolist()
        print('---',type(col))
        print(col)
        print('-------------------')
        col_types = df.dtypes
        print(col_types)
        print('-------------------')
        cursor = con.cursor()
        cursor.execute("select * from tableone limit 0")
        print('--  ', cursor.fetchall())
        cursor.execute("select * from {0}.{1} LIMIT 0".format(schema, table)) 
        # cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{1}' and table_schema = '{0}'".format(schema, table)) 
        colnames = [desc[0].replace('_', ' ') for desc in cursor.description]
        print('loggs', cursor.fetchall())
        print(colnames)
        if(not compareColumns(col, colnames)):
            raise Exception('Not matching columns')
        compareColumns(col, colnames)
        # cursor.execute("insert into schemaone.tableone (employee_id, site, payment_amount, hours, week_date) values ('2','asdf','34', '23', 'sdf')")
        if table == 'tableone':
            for index, row in df.iterrows():
                cursor.execute("INSERT into "+schema+".tableone (employee_id, site, payment_amount, hours, week_date) values (%s, %s, %s, %s, %s)", (row[col[0]], row[col[1]], row[col[2]], row[col[3]], row[col[4]]))
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
        uploaded = str(e)

    response = jsonify({"statusCode": 200, "body": {"message": uploaded}})
    return response


def compareColumns(fileColumns, dbColumns):
    fileLength = len(fileColumns)
    dbLength = len(dbColumns)
    fileIndex, dbIndex = 0, 0
    while fileIndex < fileLength and dbIndex < dbLength :
        if(fileColumns[fileIndex].lower() != dbColumns[dbIndex].lower()):
            raise Exception("Expected '{0}' column but found '{1}' column in the file".format(dbColumns[dbIndex], fileColumns[fileIndex].lower()))
        fileIndex += 1
        dbIndex += 1
    return True;

if __name__ == "__main__":
    app.run(debug=True)
