import json
from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)

# selected courses
wish_list = []
search_res = []


@app.route('/')
def welcome_page():
    return render_template('welcome.html')

# submitted search keywords
@app.route('/search', methods=['POST','GET'])
def search():
    json_data = request.get_json()
    # TODO search_courses function:
    # search_res = search_courses(json_data)
    search_res.append(json_data + " result" )
    return render_template('search_page.html', data = json_data)

# submitted search keywords
@app.route('/search_page')
def search_page():
    return render_template('search_page.html', data = search_res)

# add to wish list
@app.route('/add_wishlist')
def add_wishlist():
    json_data = request.get_json() 
    wish_list.append(json_data)
    return render_template('.html')


if __name__ == '__main__':
   app.run(debug = True)
