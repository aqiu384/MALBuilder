from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, \
    DateField, DecimalField, PasswordField, FieldList, widgets, FormField
from wtforms.validators import DataRequired, Optional, NumberRange
from src.constants import AA_TYPE, AA_STATUS, ANIME_ATTRS, AA_GENRES, MAL_STATUS


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me', default=False)


# class AddAnimeSubform():
#     def __init__(self, result):
#         self.result = result
#         setattr(self, 'addAnime' + str(self.result.malId),
#                 SelectField('Watch status', choices=list(MAL_STATUS.items())))
#
#     def get_form(self):
#         return getattr(self, 'addAnime' + str(self.result.malId))


class AddAnimeSubform(Form):
    kale = StringField('Why')
    place = StringField('Why not?')


class AddAnimeForm(Form):
    anime = []
    authors = FieldList(FormField(AddAnimeSubform))

    def __init__(self, anime_list):
        for anime in anime_list:
            self.authors.append_entry()
            self.anime.append(anime)


class AnimeSearchForm(Form):
    malIdStart = IntegerField('MAL ID start', validators=[Optional()])
    malIdEnd = IntegerField('MAL ID end', validators=[Optional()])
    type = SelectMultipleField('Type', choices=list(AA_TYPE.items()), coerce=int, validators=[Optional()])
    status = SelectMultipleField('Status', choices=list(AA_STATUS.items()), coerce=int, validators=[Optional()])
    genresInclude = SelectMultipleField('Include genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        coerce=int, validators=[Optional()])
    genresExclude = SelectMultipleField('Exclude genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        coerce=int, validators=[Optional()])
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
