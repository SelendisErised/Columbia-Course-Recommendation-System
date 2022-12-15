import json
from flask import Flask, request
from dbfunction import DatabaseConnection, ExtraInfo

host = 'lioncoursedatabase.c5zzynku9kw4.us-east-2.rds.amazonaws.com'
database_user_id = 'LionCourseAdmin'
database_user_password = 'Rivendell'
# host = 'localhost'
# database_user_id = 'root'
# database_user_password = 'hx687099'
default_scheme = '6156_Project'

# New cursor each time to make connection stable and safe
def create_cursor(host = host, database_user_id = database_user_id, database_user_password = database_user_password, default_scheme = default_scheme):
    db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
    cur, conn = db.connection()
    return cur, conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rivendell'

@app.route('/message', methods=['GET'])
def get_all_message():
    cur, conn = create_cursor()
    sql = "select * from {0}.message".format(default_scheme)
    cur.execute(sql)
    query_output = cur.fetchall()
    json_out = json.dumps([{'Email': message[0], 
                            'Time': message[1], 
                            'Content': message[2]} 
                            for message in query_output])
    json_out = json.loads(json_out)
    return json_out

@app.route('/message/<email>', methods=['GET', 'DELETE'])
def get_my_message(email):
    if request.method == 'GET':
        cur, conn = create_cursor()
        sql = "select * from {0}.message where email = '{1}'".format(default_scheme, email)
        cur.execute(sql)
        query_output = cur.fetchall()
        json_out = json.dumps([{'Email': message[0], 
                                'Time': message[1], 
                                'Content': message[2]} 
                                for message in query_output])
        json_out = json.loads(json_out)
        return json_out
    elif request.method == 'DELETE':
        cur, conn = create_cursor()
        sql = "delete from {0}.message where email = '{1}'".format(default_scheme, email)
        cur.execute(sql)
        conn.commit()
        return f'Delete all messages from email:{email}'

@app.route('/message/<email>/<time>', methods=['DELETE'])
def delete_message(email, time):
    cur, conn = create_cursor()
    try:
        sql = "delete from {0}.message where email = '{1}' and time = '{2}'".format(default_scheme, email, time)
        cur.execute(sql)
        conn.commit()
        rsp = cur.fetchall()
        return 'Delete Message Successfully'
    except:
        return 'Delete Message Unsuccessfully'

@app.route('/message/<email>/<time>/<message>', methods=['POST'])
def post_message(email, time, message):
    cur, conn = create_cursor()
    try:
        sql = "insert into {0}.message(email, time, message) values('{1}', '{2}', '{3}')".format(default_scheme, email, time, message)
        cur.execute(sql)
        conn.commit()
        rsp = cur.fetchall()
        return 'Post Message Successfully'
    except:
        return 'Post Message Unsuccessfully'

if __name__ == '__main__':
    app.run(debug = True, port=5003)