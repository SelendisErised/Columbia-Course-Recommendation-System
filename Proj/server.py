import json
from flask import Flask, request, jsonify, redirect, url_for, Response, abort
from flask import render_template
from dbfunction import DatabaseConnection, SearchFunction
from flask_login import LoginManager , login_required , UserMixin , login_user, current_user

host = 'localhost'
database_user_id = 'root'
database_user_password = 'hx687099'
default_scheme = '6156_project'

db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
cur = db.connection()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rivendell'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

message = ''

class User(UserMixin):
    def __init__(self, username, password, id, active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0
    
    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)
    
    def get_user(self, username):
        return self.users.get(username)
    
    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)
    
    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()

@app.route('/')
def welcome_page():
    return render_template('welcome.html')

@login_manager.user_loader
def load_user(user_id):
    return users_repository.get_user(user_id)

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_repository.users.keys():
            return render_template('welcome.html', message = 'Username Exists! Try another one.')
        else:
            new_user = User(username , password , users_repository.next_index())
            users_repository.save_user(new_user)
            return render_template('welcome.html', message = 'Register successfully!')
    else:
        return Response('''
            <form action="" method="post">
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=submit value=Login>
            </form>
        ''')

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registeredUser = users_repository.get_user(username)
        # print('Users '+ str(users_repository.users))
        if registeredUser != None and registeredUser.password == password:
            print('Logged in..')
            login_user(registeredUser)
            return render_template('welcome.html', message = 'Log in successfully!')
        else:
            return render_template('welcome.html', message = 'Wrong Username or Password!')
    else:
        return Response('''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')


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
