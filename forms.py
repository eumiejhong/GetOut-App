from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    """Sign Up Form for users"""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[Length(min=6)])
    state = StringField('State', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login Form for users"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for user to edit their profile"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[Length(min=6)])
    state = StringField('State', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    bio = StringField('(Optional) Tell us about yourself!')

class StoryForm(FlaskForm):
    """Form to add or edit story"""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

