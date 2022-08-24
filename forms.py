from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    """ форма регистрации """

    email = EmailField('E-mail:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class MessageForm(FlaskForm):
    content = TextAreaField("Новое сообщение", validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('Отправить')
