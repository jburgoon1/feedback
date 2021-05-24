from flask import Flask, request, render_template, redirect, session
from models import User, connect_db, db, Feedback
from forms import addUser, loginForm, feedbackForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'feedback_app'

connect_db(app)
db.create_all()

@app.route('/')
def show_register():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def show_register_form():
    form = addUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User(username = username, password = hashed, first_name = first_name, last_name = last_name, email = email)
        
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = username
        return redirect(f'/user/{username}')
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET','POST'])
def show_login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.query.filter_by(username = username).first()
        
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            session['user_id'] = username
            return redirect(f'/user/{username}')
        else:
            return False
        
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/user/<username>')
def show_secret(username):
    users = User.query.get_or_404(username)
    if "user_id" not in session:
        
        return redirect("/")
    else:
        return render_template('user.html', users = users)

@app.route("/user/<username_id>/delete")
def delete_user(username_id):
    username = User.query.get_or_404(username_id)
    db.session.delete(username)
    db.session.commit()
    session.pop('user_id')
    return redirect('/')


@app.route('/user/<username>/feedback/add', methods = ['GET', 'POST'])
def feedback_form(username):
    user = User.query.get_or_404(username)
    form = feedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title = title, content = content, user = user)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/user/{username}')

    return render_template('feedback.html', user = user, form = form)

@app.route("/user/feedback/<feedback_id>/update", methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = feedbackForm(obj = feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/user/{feedback.user.username}')
    return render_template('feedback.html', form = form)

@app.route('/user/feedback/<feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/user/{feedback.user.username}')

    # DetachedInstanceError: Parent instance <Feedback at 0x7fc6a06a23a0> is not bound to a Session; lazy load operation of attribute 'user' cannot proceed



