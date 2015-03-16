from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, \
    DateField, DecimalField, PasswordField, FieldList, widgets, FormField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Optional, NumberRange, AnyOf
from src.constants import AA_TYPE, AA_STATUS, ANIME_ATTRS, AA_GENRES, MAL_STATUS, ANIME_USER_ATTRS


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me', default=False)


class AddAnimeSubform(Form):
    result = None
    malId = IntegerField(widget=widgets.HiddenInput())
    status = SelectField('Watch status',
                         choices=list(MAL_STATUS.items()),
                         widget=widgets.ListWidget(prefix_label=False),
                         option_widget=widgets.RadioInput(),
                         coerce=int)

    def init_result(self, result):
        self.result = result


class AddAnimeForm(Form):
    subforms = FieldList(FormField(AddAnimeSubform))
    submit = SubmitField('Add anime')

    def init_results(self, results):
        for result in results:
            self.subforms.append_entry(['hello', 'goodbye'])
            self.subforms.entries[-1].init_result(result)


class UpdateAnimeSubform(Form):
    result = None
    malId = IntegerField(widget=widgets.HiddenInput())
    score = DecimalField('My Score', validators=[NumberRange(1, 10), Optional()])

    def init_result(self, result):
        self.result = result


class UpdateAnimeForm(Form):
    subforms = FieldList(FormField(UpdateAnimeSubform))
    submit = SubmitField('Update anime')

    def init_results(self, results):
        for result in results:
            self.subforms.append_entry(['hello', 'goodbye'])
            self.subforms.entries[-1].init_result(result)


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

    submit = SubmitField('Search Anime')


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
