from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField)


class addUser(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    username = StringField("Username")
    password = PasswordField("Password")
    email = StringField("Email")

class loginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")


class feedbackForm(FlaskForm):
    title = StringField("Title")
    content = StringField("Description")