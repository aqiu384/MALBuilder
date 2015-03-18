from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, \
    DateField, DecimalField, PasswordField, widgets, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from src.constants import AA_TYPE, AA_STATUS, ANIME_ATTRS, AA_GENRES, MAL_STATUS, ANIME_USER_ATTRS
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
    'myScore': lambda x: IntegerField('My Score', validators=[NumberRange(0, 10)], default=x.get('myScore')),
    'myEpisodes': lambda x: IntegerField('Episodes Watched',
                                         validators=[NumberRange(0, x.get('episodes'))],
                                         default=x.get('myEpisodes'))
}


class AnimeSubform(Form):
    """Represents a subform for a single anime"""
    pass


class MultiAnimeForm(Form):
    @staticmethod
    def createForm(results, form_fields, form_submit, mal_id):
        """Initialize a form for the given field types prepopulated with results"""
        form = MultiAnimeForm
        form.malId = mal_id

        for i, result in enumerate(results):
            for key in form_fields:
                setattr(form, '{:s}_{:d}'.format(key, i), form_fields[key](result))

        form.count = len(results)
        form.submit = SubmitField(form_submit)

        return form

    def getSubforms(self, form_fields):
        """Get all fields tied to a single anime entry"""
        for i in range(self.count):
            subform = AnimeSubform
            for key in form_fields:
                setattr(subform, key, getattr(self, '{:s}_{:d}'.format(key, i), None))
            yield subform

    def getUtoa(self, form_fields):
        """Get all results tied to a single anime entry in UserToAnime form"""
        results = []
        for i in range(self.count):
            result = UserToAnime(
                self.malId,
                self.data['malId_{}'.format(i)]
            )

            for key in form_fields:
                setattr(result, key, self.data['{:s}_{:d}'.format(key, i)])

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
