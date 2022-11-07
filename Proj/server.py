import json
from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from dbfunction import DatabaseConnection, SearchFunction

host = 'localhost'
database_user_id = 'root'
database_user_password = 'dbuserdbuser'
default_scheme = '6156_project'

db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
cur = db.connection()

app = Flask(__name__)

# selected courses

@app.route('/')
def welcome_page():
    return render_template('welcome.html')

# redirect to search page without search key
@app.route('/search_page')
def search_page_null():
    # json_data = request.get_json()
    # TODO search_courses function:
    # search_res = search_courses(json_data)
    # search_res.append(json_data + " result" )
    # return redirect(url_for('search_page.html'))
    query_output = [] # null input
    return render_template('search_page.html', data = query_output)

@app.route('/search', methods=['POST','GET'])
def search():
    json_data = request.get_json()
    # TODO search_courses function:
    # search_res = search_courses(json_data)
    # search_res.append(json_data + " result" )
    return redirect(url_for('search_page', search_key = json_data))

# submitted search keywords
@app.route('/search_page/<search_key>')
def search_page(search_key):
    search_engine = SearchFunction(default_scheme, 'Course_info')
    sql = search_engine.ambiguous_search(search_key)
    cur.execute(sql)
    query_output = cur.fetchall()
<<<<<<< HEAD
    json_data = json.dumps([{'Course': course[2], 'Number': course[0], 'Term': course[4], 'Instructor': course[5], 'Time': course[7], 'Location': course[8], 'Tag': course[9]} for course in query_output], indent=4)
    return render_template('search_page.html', data = json_data)
=======
    json_data = json.dumps([{'Course': course[2], 'Number': course[0], 'Term': course[4], 'Instructor': course[5], 'Time': course[7], 'Location': course[8]} for course in query_output], indent=4)
    json_out = json.loads(json_data)
    return render_template('search_page.html', data = json_out)

# submitted planner's search keywords and return qualified search res
@app.route('/planner_page/<search_key>')
def planner_search(search_key):
    search_engine = SearchFunction(default_scheme, 'Course_info')
    sql = search_engine.ambiguous_search(search_key)
    cur.execute(sql)
    query_output = cur.fetchall()
    return render_template('planner_page.html', data = query_output)

# redirect to planner
@app.route('/planner_page')
def planner_page():
    # search_engine = SearchFunction(default_scheme, 'Course_info')
    # sql = search_engine.ambiguous_search(search_key)
    # cur.execute(sql)
    # query_output = cur.fetchall()
    query_output = [] # null input
    return render_template('planner_page.html', data = query_output)
>>>>>>> my-backup

# add to wish list
@app.route('/add_wishlist')
def add_wishlist():
    json_data = request.get_json() 
    return render_template('.html')

if __name__ == '__main__':
   app.run(debug = True)
