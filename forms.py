from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField,TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Форма авторизации"""
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Форма регистрации"""
    user_name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email адрес', validators=[DataRequired(), Email()])
    password_hash = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired()])
    accept_tos = BooleanField('Я принимаю лицензионное соглашение', validators=[DataRequired()])
    submit = SubmitField('Создать учетную запись')


class AddbookForm(FlaskForm):
    """Форма добавления автомобиля"""
    name = StringField('Название книги', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    info = TextAreaField('Краткое содержание', validators=[DataRequired()])
    library_id = SelectField('Название библиотеки', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить книгу')


class AddDealerForm(FlaskForm):
    """Добавление дилерского центра"""
    name = StringField('Название', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Добавить библиотеку')


class SearchPriceForm(FlaskForm):
    """Форма поиска по цене"""
    start_price = IntegerField('Минимальная цена', validators=[DataRequired()], default=100)
    end_price = IntegerField('Максимальная цена', validators=[DataRequired()], default=200)
    submit = SubmitField('Поиск')


class SearchDealerForm(FlaskForm):
    """Форма поиска по дилерскому центру"""
    library_id = SelectField('Номер библиотеки', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Поиск')
