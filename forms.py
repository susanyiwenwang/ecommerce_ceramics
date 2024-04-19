from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class BillingForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    line_1 = StringField("Address Line 1", validators=[DataRequired()])
    line_2 = StringField("Address Line 2")
    city = StringField("City", validators=[DataRequired()])
    postal_code = StringField("Postal Code", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Continue to Payment")


