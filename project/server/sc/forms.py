# project/server/sc/forms.py

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class ScSearchForm(Form):
    """Home Search bar - uses autocomplete and view func"""

    search_bar = TextField('Search Soundcloud', [DataRequired()],
                             id='search-field', render_kw={'placeholder': 'Search for an artist'})
