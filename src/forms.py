from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, \
    DateField, DecimalField, PasswordField, widgets, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from src.constants import AA_TYPE, AA_STATUS, ANIME_ATTRS, AA_GENRES, MAL_STATUS, ANIME_USER_ATTRS, MAL_STATUS2, \
    date_to_string, MAL_SCORE
from src.models import UserToAnime


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me', default=False)


ADD_ANIME_FIELDS = {
    'result': lambda x: x,
    'malId': lambda x: IntegerField(widget=widgets.HiddenInput(), default=x.get('malId')),
    'myStatus': lambda x: SelectField('Watch status',
                                      choices=list(MAL_STATUS.items()),
                                      widget=widgets.ListWidget(prefix_label=False),
                                      option_widget=widgets.RadioInput(),
                                      coerce=int, default=10)
}

UPDATE_ANIME_FIELDS = {
    'result': lambda x: x,
    'malId': lambda x: IntegerField(widget=widgets.HiddenInput(), default=x.get('malId')),
    # 'myScore': lambda x: SelectField('My Score',
    #                                  choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4),
    #                                           ('5', 5), ('6', 6), ('7', 7), ('8', 8),
    #                                           ('9', 9), ('10', 10)],
    #                                  default=x.get('myScore')),
    'myScore': lambda x: SelectField('My Score',
                                     choices=list(MAL_SCORE.items()),
                                     coerce=int, default=x.get('myScore')),
    # 'myScore': lambda x: IntegerField('My Score',
    #                                   validators=[NumberRange(0, 10)],
    #                                   default=x.get('myScore')),
    'myStatus': lambda x: SelectField('Watch status',
                                      choices=list(MAL_STATUS.items()),
                                      option_widget=widgets.RadioInput(),
                                      coerce=int, default=MAL_STATUS2[x.get('myStatus')]),

    'myEpisodes': lambda x: IntegerField('Episodes Watched',
                                         validators=[NumberRange(0, x.get('episodes'))],
                                         default=x.get('myEpisodes'))
}


class AnimeSubform(Form):
    """Represents a subform for a single anime"""
    pass


def createMultiAnimeForm(results, form_fields, form_submit, mal_id):
    """Initialize a form for the given field types prepopulated with results"""
    class M(Form):
        def getSubforms(self, ff):
            """Get all fields tied to a single anime entry"""
            for j in range(self.count):
                subform = AnimeSubform
                for k in ff:
                    setattr(subform, k, getattr(self, '{:s}_{:d}'.format(k, j), None))
                yield subform

    M.malId = mal_id

    for i, result in enumerate(results):
        for key in form_fields:
            setattr(M, '{:s}_{:d}'.format(key, i), form_fields[key](result))

    M.count = len(results)
    M.submit = SubmitField(form_submit)

    return M


def getMultiAnimeUtoa(form, form_fields):
    """Get all results tied to a single anime entry in UserToAnime form"""
    results = []
    for i in range(form.count):
        result = UserToAnime(
            form.malId,
            form.data['malId_{}'.format(i)]
        )

        for key in form_fields:
            setattr(result, key, form.data['{:s}_{:d}'.format(key, i)])

        results.append(result)
    return results


class AnimeSearchForm(Form):
    malIdStart = IntegerField('MAL ID start', validators=[Optional()])
    malIdEnd = IntegerField('MAL ID end', validators=[Optional()])
    type = SelectMultipleField('Type', choices=list(AA_TYPE.items()),
                               widget=widgets.ListWidget(prefix_label=False),
                               option_widget=widgets.CheckboxInput(),
                               coerce=int, validators=[Optional()])
    status = SelectMultipleField('Status', choices=list(AA_STATUS.items()),
                                 widget=widgets.ListWidget(prefix_label=False),
                                 option_widget=widgets.CheckboxInput(),
                                 coerce=int, validators=[Optional()])
    genresInclude = SelectMultipleField('Include genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        widget=widgets.ListWidget(prefix_label=False),
                                        option_widget=widgets.CheckboxInput(),
                                        coerce=int, validators=[Optional()])
    genresExclude = SelectMultipleField('Exclude genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        widget=widgets.ListWidget(prefix_label=False),
                                        option_widget=widgets.CheckboxInput(),
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

    fields = SelectMultipleField('Return fields', choices=list(ANIME_ATTRS.items()),
                                 widget=widgets.ListWidget(prefix_label=False),
                                 option_widget=widgets.CheckboxInput(),
                                 default=list(ANIME_ATTRS.keys()),
                                 validators=[DataRequired()])

    submit = SubmitField('Search anime')

    def get_data(self):
        my_data = self.data
        date_fields = ['startDateStart', 'startDateEnd', 'endDateStart', 'endDateEnd']

        for field in date_fields:
            my_data[field] = date_to_string(my_data[field])

        return my_data


class AnimeFilterForm(Form):
    malIdStart = IntegerField('MAL ID start', validators=[Optional()])
    malIdEnd = IntegerField('MAL ID end', validators=[Optional()])
    type = SelectMultipleField('Type', choices=list(AA_TYPE.items()),
                               widget=widgets.ListWidget(prefix_label=False),
                               option_widget=widgets.CheckboxInput(),
                               coerce=int, validators=[Optional()])
    showStatus = SelectMultipleField('Show Status', choices=list(AA_STATUS.items()),
                                     widget=widgets.ListWidget(prefix_label=False),
                                     option_widget=widgets.CheckboxInput(),
                                     coerce=int, validators=[Optional()])
    myStatus = SelectMultipleField('My Status', choices=list(MAL_STATUS.items()),
                                   widget=widgets.ListWidget(prefix_label=False),
                                   option_widget=widgets.CheckboxInput(),
                                   coerce=int, validators=[Optional()])
    genresInclude = SelectMultipleField('Include genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        widget=widgets.ListWidget(prefix_label=False),
                                        option_widget=widgets.CheckboxInput(),
                                        coerce=int, validators=[Optional()])
    genresExclude = SelectMultipleField('Exclude genres',
                                        choices=sorted(list(AA_GENRES.items()), key=lambda x: x[1]),
                                        widget=widgets.ListWidget(prefix_label=False),
                                        option_widget=widgets.CheckboxInput(),
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
    episodeGreaterThan = IntegerField('Episode count start', validators=[Optional()])
    episodeLessThan = IntegerField('Episode count end', validators=[Optional()])
    episodeWatchedStart = IntegerField('Episode watched start', validators=[Optional()])
    episodeWatchedEnd = IntegerField('Episode watched end', validators=[Optional()])
    myWatchDateStart = DateField('Started Watching', format='%m/%d/%Y', validators=[Optional()])
    myWatchDateEnd = DateField('Finished Watching', format='%m/%d/%Y', validators=[Optional()])
    myScoreStart = DecimalField('my score start', validators=[NumberRange(1, 10), Optional()])
    myScoreEnd = DecimalField('my score end', validators=[NumberRange(1, 10), Optional()])
    rewatchEpisodesStart = IntegerField('episode rewatched start', validators=[Optional()])
    rewatchEpisodesEnd = IntegerField('episode rewatched end', validators=[Optional()])
    updateDateStart = DateField('update date start', format='%m/%d/%Y', validators=[Optional()])
    updateDateEnd = DateField('update date end', format='%m/%d/%Y', validators=[Optional()])

    fields = SelectMultipleField('Return fields', choices=list(ANIME_USER_ATTRS.items()),
                                 widget=widgets.ListWidget(prefix_label=False),
                                 option_widget=widgets.CheckboxInput(),
                                 default=list(ANIME_USER_ATTRS.keys()),
                                 validators=[DataRequired()])

    submit = SubmitField('Filter Anime')

    def get_data(self):
        my_data = self.data
        date_fields = ['startDateStart', 'startDateEnd', 'endDateStart', 'endDateEnd',
                       'updateDateStart', 'updateDateEnd']

        for field in date_fields:
            my_data[field] = date_to_string(my_data[field])

        return my_data

class AnichartForm(Form):
    startDateStart = DateField('Year', format='%Y', validators=[Optional()])
    season = SelectField('Season Aired',
                        choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'), ('Winter', 'Winter')],
                        validators=[Optional()])
    submit = SubmitField('You should just go to Anichart instead')


class FlashcardSeasonForm(Form):
    year = DateField('Year', format='%Y', validators=[DataRequired()])
    season = SelectField('Season',
                         choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall')],
                         validators=[DataRequired()])


class FlashcardForm(Form):
    anime_id = IntegerField('MAL ID', validators=[DataRequired()])
    status = SelectField('Watch Status', choices=list(MAL_STATUS.items()), coerce=int, default=10)


def createMultiAnimeForm(results, form_fields, form_submit, mal_id):
    """Initialize a form for the given field types prepopulated with results"""
    class M(Form):
        def getSubforms(self, ff):
            """Get all fields tied to a single anime entry"""
            for j in range(self.count):
                subform = AnimeSubform
                for k in ff:
                    setattr(subform, k, getattr(self, '{:s}_{:d}'.format(k, j), None))
                yield subform

    M.malId = mal_id

    for i, result in enumerate(results):
        for key in form_fields:
            setattr(M, '{:s}_{:d}'.format(key, i), form_fields[key](result))

    M.count = len(results)
    M.submit = SubmitField(form_submit)

    return M


def get_update_forms(utoa_list):
    return [UpdateAnimeForm(x) for x in utoa_list]


def UpdateAnimeForm(utoa):
    class M(Form):
        pass

    M.result = utoa
    M.malId = IntegerField('Anime ID',
                           widget=widgets.HiddenInput(),
                           default=utoa.malId,
                           validators=[DataRequired()])
    M.myScore = SelectField('My Score',
                            choices=list(MAL_SCORE.items()),
                            coerce=int,
                            default=utoa.myScore,
                            validators=[Optional()])
    M.myStatus = SelectField('Watch status',
                             choices=list(MAL_STATUS.items()),
                             coerce=int,
                             default=utoa.myStatus,
                             validators=[Optional()])
    M.myEpisodes = IntegerField('Episodes Watched',
                                default=utoa.myEpisodes,
                                validators=[Optional(), NumberRange(0, utoa.episodes)])

    return M