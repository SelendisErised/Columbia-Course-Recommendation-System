from flask_login import LoginManager , login_required , UserMixin , login_user, current_user

class User(UserMixin):
    
    def __init__(self, username, password, openid):
        self.id = openid
        self.username = username
        self.password = password
        self.course = []

    def get_id(self):
        return self.openid

    def is_active(self):
        return self.active

    def update_course(self, course_list):
        self.course.extend(course_list)

    def get_course(self):
        return self.course

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0
    
    def save_user(self, user):
        self.users_id_dict.setdefault(user.openid, user)
        self.users.setdefault(user.username, user)
    
    def get_user(self, username):
        return self.users.get(username)
    
    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)
    
    def next_index(self):
        self.identifier +=1
        return self.identifier