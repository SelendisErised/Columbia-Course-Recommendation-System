import json
from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from dbfunction import DatabaseConnection, SearchFunction

host = 'localhost'
database_user_id = 'root'
database_user_password = 'hx687099'
default_scheme = '6156_project'

db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
cur = db.connection()

app = Flask(__name__)

# selected courses

@app.route('/')
def welcome_page():
    return render_template('welcome.html')

# submitted search keywords
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
    return render_template('search_page.html', data = query_output)

# add to wish list
@app.route('/add_wishlist')
def add_wishlist():
    json_data = request.get_json() 
    return render_template('.html')

if __name__ == '__main__':
   app.run(debug = True)
