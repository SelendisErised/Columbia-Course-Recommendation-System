from flask import Flask, request
from dbfunction import DatabaseConnection, ExtraInfo

host = 'lioncoursedatabase.c5zzynku9kw4.us-east-2.rds.amazonaws.com'
database_user_id = 'LionCourseAdmin'
database_user_password = 'Rivendell'
default_scheme = '6156_Project'

def create_cursor(host = host, database_user_id = database_user_id, database_user_password = database_user_password, default_scheme = default_scheme):
    db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
    cur, conn = db.connection()
    return cur, conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rivendell'

@app.route('/department/<course_prefix>', methods=['GET'])
def get_department(course_prefix):
    cur, conn = create_cursor()
    search_engine = ExtraInfo(default_scheme, cur, conn)
    json_out = search_engine.prefix_to_department(course_prefix)
    return json_out

if __name__ == '__main__':
    app.run(debug = True, port=5000)