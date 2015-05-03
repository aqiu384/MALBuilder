from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectMultipleField, IntegerField, \
    DateField, DecimalField, PasswordField, widgets, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from src.constants import AA_TYPE, AA_STATUS, ANIME_ATTRS, AA_GENRES, MAL_STATUS, ANIME_USER_ATTRS, MAL_STATUS2, \
    date_to_string, MAL_SCORE
from src.models import UserToAnime


class LoginForm(Form):
    """Represents a user login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me', default=False)


# Add Anime form field to generate
ADD_ANIME_FIELDS = {
    'result': lambda x: x,
    'malId': lambda x: IntegerField(widget=widgets.HiddenInput(), default=x.get('malId')),
    'myStatus': lambda x: SelectField('Watch status',
                                      choices=list(MAL_STATUS.items()),
                                      widget=widgets.ListWidget(prefix_label=False),
                                      option_widget=widgets.RadioInput(),
                                      coerce=int, default=10)
}


def createMultiAnimeForm(results, form_fields, form_submit, mal_id):
    """
    Initialize a form for the given field types prepopulated with results

    :param results: Anime Results list to include in form
    :param form_fields: Fields to display
    :param form_submit: Name of submit button to create
    :param mal_id: User's MAL ID
    :return: MultiAnimeForm initialized with parsed results
    """

    class M(Form):
        def getSubforms(self, ff):
            """Get all fields tied to a single anime entry"""

            class AnimeSubform(Form):
                """Represents a subform for a single anime"""
                pass

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
    """
    Get all results tied to a single anime entry in UserToAnime form

    :param form: MultiAnimeForm to parse
    :param form_fields: Fields to include
    :return: User to Anime list containing parsed data
    """
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
    """Represents an Search Form for anime the User has not searched before"""
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
        """
        Get a list of data contained by the form in printable format

        :return: List of form data
        """
        my_data = self.data
        date_fields = ['startDateStart', 'startDateEnd', 'endDateStart', 'endDateEnd']

        for field in date_fields:
            my_data[field] = date_to_string(my_data[field])

        return my_data


class AnimeFilterForm(Form):
    """Represents an Filter Form for the user's MAL"""
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
                                   coerce=int, validators=[Optional()], default=[1, 2, 3, 4, 6])
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
                                 default=['title', 'description', 'myScore', 'score', 'imgLink'],
                                 validators=[DataRequired()])

    submit = SubmitField('Filter Anime')

    def get_data(self):
        """
        Get a list of data contained by the form in printable format

        :return: List of form data
        """
        my_data = self.data
        date_fields = ['startDateStart', 'startDateEnd', 'endDateStart', 'endDateEnd',
                       'updateDateStart', 'updateDateEnd']

        for field in date_fields:
            my_data[field] = date_to_string(my_data[field])

        return my_data


class AnichartForm(Form):
    """Represents a search form for retrieving Anicharts results by season"""
    startDateStart = DateField('Year', format='%Y', validators=[DataRequired()])
    season = SelectField('Season Aired',
                         choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'), ('Winter', 'Winter')],
                         validators=[DataRequired()])
    submit = SubmitField('You should just go to Anichart instead')


class FlashcardSeasonForm(Form):
    """Represents a search form for sorting Flashcard add results"""
    year = DateField('Year', format='%Y', validators=[DataRequired()])
    season = SelectField('Season',
                         choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall')],
                         validators=[DataRequired()])


class FlashcardForm(Form):
    """Represents a Flashcard Form for adding anime"""
    anime_id = IntegerField('MAL ID', validators=[DataRequired()])
    status = SelectField('Watch Status', choices=list(MAL_STATUS.items()), coerce=int, default=10)


def get_update_forms(utoa_list):
    """
    Generates a list of Update forms for each entry in the anime list

    :param utoa_list: List of anime to create forms for
    :return: List of UpdateAnimeForms
    """
    return [UpdateAnimeForm(x) for x in utoa_list]


def UpdateAnimeForm(utoa):
    """Represents an Update Anime form with the given anime for validation requirements"""
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
    M.myStartDate = DateField('Date Started',
                              default=utoa.myStartDate,
                              format='%m/%d/%Y',
                              validators=[Optional()])
    M.myEndDate = DateField('Date Completed',
                            default=utoa.myEndDate,
                            format='%m/%d/%Y',
                            validators=[Optional()])
    M.myRewatchEps = IntegerField('Rewatched Episodes',
                                  default=utoa.myRewatchEps,
                                  validators=[Optional()])

    return M