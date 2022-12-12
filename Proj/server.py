import json
import requests
from flask import Flask, request, jsonify, redirect, url_for, Response, abort, g, session, flash
from flask import render_template
from dbfunction import DatabaseConnection, SearchFunction, EvaluationFunction
# from flask_login import LoginManager , login_required , UserMixin , login_user, current_user
# from user import User, UsersRepository
# from flask_openid import OpenID
from flask_oauth import OAuth

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
# oid = OpenID(app, '/path/to/store', safe_roots=[])

oauth = OAuth()
GOOGLE_CLIENT_ID = "604932245172-af2apa8g3sr5fa7rbivsb7744qaljtp6.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = '/callback'  # one of the Redirect URIs from Google APIs console
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                        #   request_token_params={'scope': 'openid profile https://www.googleapis.com/auth/userinfo.email',
                          request_token_params={'scope': 'openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

# GOOGLE_CLIENT_ID = "604932245172-af2apa8g3sr5fa7rbivsb7744qaljtp6.apps.googleusercontent.com"
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# login_manager = LoginManager()
# login_manager.login_view = "login"
# login_manager.init_app(app)

# message = ''
# users_repository = UsersRepository()

# @app.route('/')
# def welcome_page():
#     access_token = session.get('access_token')
#     if access_token is None:
#         return redirect(url_for('login'))
#     return render_template('welcome.html', data=session.get('resp_obj'))

# @app.route('/login')
# def login():
#     callback=url_for('authorized', _external=True)
#     return google.authorize(callback=callback)

# @app.route(REDIRECT_URI)
# @google.authorized_handler
# def authorized(resp):
#     access_token = resp['access_token']
#     session['access_token'] = access_token, ''
#     session['resp_obj'] = resp
#     return redirect(url_for('welcome_page'))

# @google.tokengetter
# def get_access_token():
#     return session.get('access_token')

@app.route('/')
def welcome_page():
    return render_template('welcome.html')

# Main Functions and Features 

# redirect to search page without search key
@app.route('/search_page')
def search_page_null():
    query_output = [] # null input
    return render_template('search_page.html', data = query_output)

@app.route('/search', methods=['POST','GET'])
def search():
    json_data = request.get_json()
    return redirect(url_for('search_page', search_key = json_data))

# submitted search keywords
@app.route('/search_page/<search_key>')
def search_page(search_key):
    result = requests.get(f'http://127.0.0.1:5001/search_page/{search_key}')
    return render_template('search_page.html', data = result.json())
#     cur, conn = create_cursor()
#     search_engine = SearchFunction(default_scheme, 'Course_info', cur)
#     json_out = search_engine.ambiguous_search(search_key)
#     conn.close()
#     return render_template('search_page.html', data = json_out)


# wish_list = ['COMS6998E00120223', 'COMS6998E00220223']
wish_list =[]
# submitted planner's search keywords and return qualified search res
@app.route('/planner_page/<search_key>')
def planner_search(search_key):
    wish_list_string = '&'.join(map(str,wish_list))
    params = search_key + "@" + wish_list_string
    print("here")
    print(params)
    result = requests.get(f'http://127.0.0.1:5001/planner_page/{params}')
    # cur, conn = create_cursor()
    # search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    # json_out = search_engine.qualify_search(wish_list, search_key)
    # search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    wish_list_info = requests.get(f'http://127.0.0.1:5001/planner_page/{params}/wish_list')
    # conn.close()
    # return render_template('planner_page.html', data = json_out, wish_list = wish_list_info)
    return render_template('planner_page.html', data = result.json(), wish_list = wish_list_info.json())

# redirect to planner
@app.route('/planner_page')
def planner_page():
    # result = requests.get(f'http://127.0.0.1:5001/search_page/{search_key}')
    query_output = [] # null input
    wish_list_info = []
    return render_template('planner_page.html', data = query_output, wish_list = wish_list_info)
    # cur, conn = create_cursor()
    # search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    # wish_list_info = search_engine.course_to_frontend_info(wish_list)
    # query_output = [] # null input
    # conn.close()
    # return render_template('planner_page.html', data = query_output, wish_list = wish_list_info)

# add to wish list
@app.route('/add_course', methods=['POST','GET'])
def add_course():
    course_number = request.get_json()
    wish_list.append(course_number)
    return ('', 204)

# remove from wish list
@app.route('/remove_course', methods=['POST','GET'])
def remove_course():
    course_number = request.get_json()
    wish_list.remove(course_number)
    return ('', 204)

@app.route('/evaluation_page')
def evaluation_page_null():
    query_output = [] # null input
    return render_template('evaluation_page.html', data = query_output)

@app.route('/rating', methods=['POST','GET'])
def rating():
    cur, conn = create_cursor()
    query = request.get_json()
    search_key, evaluation = query['search_key'], query['evaluation']
    # TODO search_courses function:
    search_engine = EvaluationFunction(default_scheme, cur, conn)
    search_engine.evaluate(search_key, evaluation)

    return redirect('/evaluation_page/' + search_key)

# submitted search keywords
@app.route('/evaluation_page/<search_key>')
def evaluation_page(search_key):
    cur, conn = create_cursor()
    search_engine = EvaluationFunction(default_scheme, cur, conn)
    json_out = search_engine.evaluation_search(search_key)

    return render_template('evaluation_page.html', data = json_out)

@app.route('/rating_page/<search_key>')
def rating_page(search_key):
    cur, conn = create_cursor()
    search_engine = EvaluationFunction(default_scheme, cur, conn)
    json_out = search_engine.evaluation_search(search_key)

    return render_template('rating_page.html', data = json_out)

@app.route('/about_page')
def about_page():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    return render_template('about.html', data=session.get('resp_obj'))

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
