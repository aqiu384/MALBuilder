from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, DateField, DecimalField, PasswordField
from wtforms.validators import DataRequired, Optional, NumberRange
from .models import AA_TYPE, AA_STATUS, ANIME_ATTRS


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me', default=False)


# class AaSearchForm(Form):
#     idiStart = IntegerField('MAL ID start', validators=[Optional()])
#     idiEnd = IntegerField('MAL ID end', validators=[Optional()])
#     idt = SelectMultipleField('Status', choices=list(zip(AA_TYPE, AA_TYPE)), validators=[Optional()])
#     title = StringField('Title keyword', validators=[Optional()])
#     airedFromStart = DateField('Aired from start', format='%m/%d/%Y', validators=[Optional()])
#     airedFromEnd = DateField('Aired from end', format='%m/%d/%Y', validators=[Optional()])
#     airedToStart = DateField('Aired to start', format='%m/%d/%Y', validators=[Optional()])
#     airedToEnd = DateField('Aired to end', format='%m/%d/%Y', validators=[Optional()])
#     episodesStart = IntegerField('Episodes start', validators=[Optional()])
#     episodesEnd = IntegerField('Episodes end', validators=[Optional()])
#     durationStart = IntegerField('Duration start', validators=[Optional()])
#     durationEnd = IntegerField('Duration end', validators=[Optional()])
#     genresInclude = SelectMultipleField('Gen include', choices=list(zip(AA_GENRE, AA_GENRE)), validators=[Optional()])
#     genresExclude = SelectMultipleField('Gen exclude', choices=list(zip(AA_GENRE, AA_GENRE)), validators=[Optional()])
#     malScoreStart = DecimalField('MAL score start', validators=[NumberRange(1, 10), Optional()])
#     malScoreEnd = DecimalField('Mal score end', validators=[NumberRange(1, 10), Optional()])
#     membersStart = IntegerField('Members ID start', validators=[Optional()])
#     membersEnd = IntegerField('Members ID end', validators=[Optional()])
#     statusInclude = SelectMultipleField('Status', choices=list(zip(AA_STATUS, AA_STATUS)), validators=[Optional()])
#
#     returnFields = SelectMultipleField('Return fields', choices=list(zip(AA_FIELD_TO_TYPE, AA_FIELD_TO_TYPE)),
#                                        validators=[DataRequired()])


class AnimeSearchForm(Form):
    malIdStart = IntegerField('MAL ID start', validators=[Optional()])
    malIdEnd = IntegerField('MAL ID end', validators=[Optional()])
    type = SelectMultipleField('Type', choices=list(AA_TYPE.items()), coerce=int, validators=[Optional()])
    status = SelectMultipleField('Status', choices=list(AA_STATUS.items()), coerce=int, validators=[Optional()])
    title = StringField('Title keyword', validators=[Optional()])
    startDateStart = DateField('Aired from start', format='%m/%d/%Y', validators=[Optional()])
    startDateEnd = DateField('Aired from end', format='%m/%d/%Y', validators=[Optional()])
    endDateStart = DateField('Aired to start', format='%m/%d/%Y', validators=[Optional()])
    endDateEnd = DateField('Aired to end', format='%m/%d/%Y', validators=[Optional()])
    scoreStart = DecimalField('MAL score start', validators=[NumberRange(1, 10), Optional()])
    scoreEnd = DecimalField('Mal score end', validators=[NumberRange(1, 10), Optional()])
    membersStart = IntegerField('Members count start', validators=[Optional()])
    membersEnd = IntegerField('Members count end', validators=[Optional()])

    fields = SelectMultipleField('Return fields', choices=list(ANIME_ATTRS.items()), validators=[DataRequired()])
