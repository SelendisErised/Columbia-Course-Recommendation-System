from flask import Flask, request, session
from dbfunction import DatabaseConnection, SearchFunction

host = 'lioncoursedatabase.c5zzynku9kw4.us-east-2.rds.amazonaws.com'
database_user_id = 'LionCourseAdmin'
database_user_password = 'Rivendell'
default_scheme = '6156_Project'

# Create a new cursor everytime or pymysql connection is lost
def create_cursor(host = host, database_user_id = database_user_id, database_user_password = database_user_password, default_scheme = default_scheme):
    db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
    cur, conn = db.connection()
    return cur, conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rivendell'

# Main Functions and Features 

# submitted search keywords
@app.route('/search/<search_key>', methods=['GET'])
def search_page(search_key):
    try:
        cur, conn = create_cursor()
        search_engine = SearchFunction(default_scheme, 'Course_info', cur)
        json_out = search_engine.ambiguous_search(search_key)
        conn.close()
        return json_out
    except:
        return 'Search Failed'

wish_list = ['COMS4111WH0220223']
wish_list_info = []

# submitted planner's search keywords and return qualified search res
@app.route('/plan/<search_param>', methods=['GET'])
def planner_search(search_param):
    search_param_list = search_param.split('@')
    search_key = search_param_list[0]
    wish_list = []
    wish_list = search_param_list[1].split('&')
    cur, conn = create_cursor()
    search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    json_out = search_engine.qualify_search(wish_list, search_key)
    # query_output = [] # null input
    conn.close()
    return json_out

@app.route('/plan/<search_param>/wish_list', methods=['GET'])
def wish_list_info_generate(search_param):
    search_param_list = search_param.split('@')
    # search_key = search_param_list[0]
    wish_list = []
    wish_list = search_param_list[1].split('&')
    if wish_list[0] == '':
        wish_list = []
    cur, conn = create_cursor()
    search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    wish_list_info = search_engine.course_to_frontend_info(wish_list)
    conn.close()
    return wish_list_info

# redirect to planner
@app.route('/plan', methods=['GET'])
def planner_page():
    cur, conn = create_cursor()
    search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    wish_list_info = search_engine.course_to_frontend_info(wish_list)
    query_output = [] # null input
    conn.close()
    return wish_list_info


if __name__ == '__main__':
    app.run(debug = True, port=5001)