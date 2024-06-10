from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class EquationsForm(FlaskForm):
    x = StringField('x = ')
    y = StringField('y = ')
    submit = SubmitField('Отправить')
    new_submit = SubmitField('Новый пример')


class ComplexsForm(FlaskForm):
    x = StringField('x1 = ')
    y = StringField('x2 = ')
    submit = SubmitField('Отправить')
    new_submit = SubmitField('Новый пример')

class TaskForm(FlaskForm):
    x = StringField('Ответ')
    submit = SubmitField('Отправить')
    new_submit = SubmitField('Новый пример')


