from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms.validators import InputRequired


class BookingForm(FlaskForm):
    name = StringField('name', [InputRequired()])
    phone = StringField('phone', [InputRequired()])


class RequestForm(FlaskForm):
    purpose = RadioField('purpose', choices=[("Для путешествий", "Для путешествий"),
                                             ("Для школы", "Для школы"),
                                             ("Для работы", "Для работы"),
                                             ("Для переезда", "Для переезда")], default='Для путешествий')
    free_time = RadioField('free_time', choices=[("1-2", "1-2 часа в неделю"),
                                                 ("3-5", "3-5 часов в неделю"),
                                                 ("5-7", "5-7 часов в неделю"),
                                                 ("7-10", "7-10 часов в неделю")], default='1-2')
    name = StringField('name', [InputRequired()])
    phone = StringField('phone', [InputRequired()])


class SortForm(FlaskForm):
    sort = SelectField('select', choices=[('1', 'В случайном порядке'),
                                          ('2', 'Сначала лучший рейтинг'),
                                          ('3', 'Сначала дорогие'),
                                          ('4', 'Сначала недорогие')])
