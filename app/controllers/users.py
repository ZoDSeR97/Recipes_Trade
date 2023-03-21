from app import app
from app.models import user, recipe
from flask import render_template, redirect, request, session

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # see if the login information provided valid
    if not user.User.validate_login(request.form):
        return redirect('/')
    user_in_db = user.User.get_one(request.form, condition='email')
    session['user_id'] = user_in_db[0].id
    # never render on a post!!!
    return redirect("/recipes")

@app.route('/register', methods=['POST'])
def register():
    if user.User.validate_registration(request.form):
        # Call the save @classmethod on User
        user.User.save(request.form)
    return redirect('/')
