from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такая почта уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')


# Форма для анкеты пользователя
class QuestionnaireForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    hobby = StringField('Любимое хобби', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=0, max=120)])
    submit = SubmitField('Отправить')


# Форма для редактирования профиля пользователя
class UpdateProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Новый пароль (оставьте пустым, если не хотите менять)', validators=[Optional()])
    confirm_password = PasswordField('Подтвердите новый пароль', validators=[Optional()])
    submit = SubmitField('Сохранить изменения')

    def validate_username(self, username):
        # Проверяем уникальность только если имя изменилось
        if current_user.is_authenticated and username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Такое имя уже существует. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        # Проверяем уникальность только если email изменился
        if current_user.is_authenticated and email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Такая почта уже используется. Пожалуйста, выберите другую.')

    def validate_password(self, password):
        # Если указан пароль, проверяем что подтверждение тоже заполнено и совпадает
        if password.data:
            if not self.confirm_password.data:
                raise ValidationError('Подтвердите новый пароль.')
            if password.data != self.confirm_password.data:
                raise ValidationError('Пароли должны совпадать.')

    def validate_confirm_password(self, confirm_password):
        # Если указано подтверждение, проверяем что пароль тоже заполнен
        if confirm_password.data and not self.password.data:
            raise ValidationError('Введите новый пароль.')