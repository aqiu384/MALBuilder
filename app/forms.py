from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, DateField, DecimalField
from wtforms.validators import DataRequired, Optional, NumberRange
from api.aasession import AA_GENRE, AA_STATUS, AA_FIELD_TO_TYPE, AA_TYPE


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class AaSearchForm(Form):
    idiStart = IntegerField('MAL ID start', validators=[Optional()])
    idiEnd = IntegerField('MAL ID end', validators=[Optional()])
    idt = SelectMultipleField('Status', choices=list(zip(AA_TYPE, AA_TYPE)), validators=[Optional()])
    title = StringField('Title keyword', validators=[Optional()])
    airedFromStart = DateField('Aired from start', format='%m/%d/%Y', validators=[Optional()])
    airedFromEnd = DateField('Aired from end', format='%m/%d/%Y', validators=[Optional()])
    airedToStart = DateField('Aired to start', format='%m/%d/%Y', validators=[Optional()])
    airedToEnd = DateField('Aired to end', format='%m/%d/%Y', validators=[Optional()])
    episodesStart = IntegerField('Episodes start', validators=[Optional()])
    episodesEnd = IntegerField('Episodes end', validators=[Optional()])
    durationStart = IntegerField('Duration start', validators=[Optional()])
    durationEnd = IntegerField('Duration end', validators=[Optional()])
    genresInclude = SelectMultipleField('Gen include', choices=list(zip(AA_GENRE, AA_GENRE)), validators=[Optional()])
    genresExclude = SelectMultipleField('Gen exclude', choices=list(zip(AA_GENRE, AA_GENRE)), validators=[Optional()])
    malScoreStart = DecimalField('MAL score start', validators=[NumberRange(1, 10), Optional()])
    malScoreEnd = DecimalField('Mal score end', validators=[NumberRange(1, 10), Optional()])
    membersStart = IntegerField('Members ID start', validators=[Optional()])
    membersEnd = IntegerField('Members ID end', validators=[Optional()])
    statusInclude = SelectMultipleField('Status', choices=list(zip(AA_STATUS, AA_STATUS)), validators=[Optional()])

    returnFields = SelectMultipleField('Return fields', choices=list(zip(AA_FIELD_TO_TYPE, AA_FIELD_TO_TYPE)),
                                       validators=[DataRequired()])