import json
from flask import Flask, request, jsonify, redirect, url_for, Response, abort, g, session, flash
from flask import render_template
from dbfunction import DatabaseConnection, SearchFunction
# from flask_login import LoginManager , login_required , UserMixin , login_user, current_user
# from user import User, UsersRepository
# from flask_openid import OpenID
from flask_oauth import OAuth

host = 'localhost'
database_user_id = 'root'
database_user_password = 'hx687099'
default_scheme = '6156_project'

db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
cur = db.connection()

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
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
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

@app.route('/')
def welcome_page():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    return render_template('welcome.html')

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('welcome_page'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

# Default Login 
# @login_manager.user_loader
# def load_user(user_id):
#     return users_repository.get_user(user_id)

# @app.route('/register', methods = ['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users_repository.users.keys():
#             return render_template('welcome.html', message = 'Username exists! Try another one.')
#         else:
#             new_user = User(username , password , users_repository.next_index())
#             users_repository.save_user(new_user)
#             return render_template('welcome.html', message = 'Register successfully!')
#     elif request.method == 'GET':
#         return render_template('register.html')
#     else:
#         pass

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         registeredUser = users_repository.get_user(username)
#         # print('Users '+ str(users_repository.users))
#         if registeredUser != None and registeredUser.password == password:
#             print('Logged in..')
#             login_user(registeredUser)
#             return render_template('welcome.html', message = 'Log in successfully!')
#         else:
#             return render_template('welcome.html', message = 'Wrong Username or Password!')
#     else:
#         return render_template('login.html')

# Openid Login 
# @app.before_request
# def lookup_current_user():
#     g.user = None
#     if 'openid' in session:
#         openid = session['openid']
#         g.user = User.query.filter_by(openid=openid).first()

# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None:
#         return redirect(oid.get_next_url())
#     if request.method == 'POST':
#         openid = request.form.get('openid')
#         if openid:
#             return oid.try_login(openid, ask_for=['email', 'nickname'],
#                                          ask_for_optional=['fullname'])
#     return render_template('login.html', next=oid.get_next_url(),
#                            error=oid.fetch_error())

# @oid.after_login
# def create_or_login(resp):
#     session['openid'] = resp.identity_url
#     user = User.query.filter_by(openid=resp.identity_url).first()
#     if user is not None:
#         flash(u'Successfully signed in')
#         g.user = user
#         return redirect(oid.get_next_url())
#     return redirect(url_for('create_profile', next=oid.get_next_url(),
#                             name=resp.fullname or resp.nickname,
#                             email=resp.email))

# @app.route('/create-profile', methods=['GET', 'POST'])
# def create_profile():
#     if g.user is not None or 'openid' not in session:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         if not name:
#             flash(u'Error: you have to provide a name')
#         elif '@' not in email:
#             flash(u'Error: you have to enter a valid email address')
#         else:
#             flash(u'Profile successfully created')
#             db_session.add(User(name, email, session['openid']))
#             db_session.commit()
#             return redirect(oid.get_next_url())
#     return render_template('create_profile.html', next=oid.get_next_url())

# @app.route('/logout')
# def logout():
#     session.pop('openid', None)
#     flash(u'You were signed out')
#     return redirect(oid.get_next_url())

# Main Functions and Features 

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
    search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    json_out = search_engine.ambiguous_search(search_key)
    return render_template('search_page.html', data = json_out)

# submitted planner's search keywords and return qualified search res
@app.route('/planner_page/<search_key>')
def planner_search(search_key):
    search_engine = SearchFunction(default_scheme, 'Course_info', cur)
    json_out = search_engine.ambiguous_search(search_key)
    return render_template('planner_page.html', data = json_out)

# redirect to planner
@app.route('/planner_page')
def planner_page():
    # search_engine = SearchFunction(default_scheme, 'Course_info')
    # sql = search_engine.ambiguous_search(search_key)
    # cur.execute(sql)
    # query_output = cur.fetchall()
    query_output = [] # null input
    return render_template('planner_page.html', data = query_output)

# add to wish list
@app.route('/add_wishlist')
def add_wishlist():
    json_data = request.get_json() 
    return render_template('.html')

if __name__ == '__main__':
    app.run(debug = True)