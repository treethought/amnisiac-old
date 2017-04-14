# project/server/reddit/forms.py

from flask_wtf import Form
from wtforms import TextField, SelectMultipleField, widgets
from wtforms.validators import Optional


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    widget = widgets.TableWidget()
    # widget = MyTableWidget()
    option_widget = widgets.CheckboxInput()


class RedditSearchForm(Form):
    """Used in sources.html - autocompletes using select2 and he multicheckbox"""

    follow_sources = MultiCheckboxField('Subs', id='select-field', validators=[Optional()])

    search_bar = TextField('Search Subreddits', id='search-bar')
