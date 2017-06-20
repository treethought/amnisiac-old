# -*- coding: utf-8 -*-
"""Public forms."""

from flask_wtf import Form
from wtforms import TextField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    widget = widgets.TableWidget()
    # widget = MyTableWidget()
    option_widget = widgets.CheckboxInput()


class HomeSearchForm(Form):
    """Used in sources.html - autocompletes using select2 and he multicheckbox"""

    follow_sources = MultiCheckboxField('Subs', id='select-field', validators=[Optional()])

    reddit_search = TextField('Search Subreddits', id='reddit-search-bar')

    sc_search = TextField('Search Soundcloud', id='sc-search-bar', render_kw={'placeholder': 'Search for an artist'})


class RedditSearchForm(Form):
    """Used in sources.html - autocompletes using select2 and he multicheckbox"""

    follow_sources = MultiCheckboxField('Subs', id='select-field', validators=[Optional()])

    reddit_search = TextField('Search Subreddits', id='search-bar')


class ScSearchForm(Form):
    """Home Search bar - uses autocomplete and view func"""

    sc_search = TextField('Search Soundcloud', [DataRequired()],
                             id='search-field', render_kw={'placeholder': 'Search for an artist'})


class MyTableWidget(widgets.TableWidget):
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """
    def __init__(self, with_table_tag=True):
        self.with_table_tag = with_table_tag

    def __call__(self, field, headers=None, thead_class=None, tr_class=None, th_class=None, td_class=None, **kwargs):
        html = []
        if self.with_table_tag:
            kwargs.setdefault('id', field.id)
            html.append('<table %s>' % widgets.html_params(**kwargs))

        if headers:
            html.append('<thead class=%s><tr>' % (thead_class))
            for h in headers:
                html.append('<th>%s</th' & (h))
            html.append('</tr></thead>')

        hidden = ''
        for subfield in field:
            print(subfield)
            if subfield.type in ('HiddenField', 'CSRFTokenField'):
                hidden += text_type(subfield)

            else:
                html.append('<tr class=%s><th class=%s>%s</th><td>%s%s</td></tr>' % (tr_class, th_class, text_type(subfield.label), hidden, text_type(subfield)))
                hidden = ''
        if self.with_table_tag:
            html.append('</table>')
        if hidden:
            html.append(hidden)
        return HTMLString(''.join(html))

