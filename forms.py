from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Email,DataRequired,InputRequired,Length

class Todo(FlaskForm):
    todo = StringField(validators=[DataRequired(),
                                   Length(min= 5)])
    submit = SubmitField("Add")
#  {{ forms.check_box(class="form-check-input my-check rounded", type="checkbox") }}

class CheckBox(FlaskForm):
    check_box = BooleanField(default=False)


class Login(FlaskForm):
    email = StringField(validators=[DataRequired(),
                                         Email(check_deliverability=True),
                                         Length(min=10), ])
    password = PasswordField(validators=[DataRequired(),
                                         Length(min=8)])
    submit = SubmitField()

class Register(FlaskForm):
    name = StringField(validators=[DataRequired(),
                                    Length(min=3)])
    email = StringField(validators=[DataRequired(),
                                    Email(check_deliverability=True),
                                    Length(min=10), ])
    password = PasswordField(validators=[DataRequired(),
                                         Length(min=8)])
    submit = SubmitField()


