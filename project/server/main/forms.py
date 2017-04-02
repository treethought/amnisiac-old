# project/server/main/forms

from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired
from project.server.scrapers.reddit_links import wiki_subs



class PostForm(Form):
    """Add new subreddit"""

    subreddit = TextField('Subreddit', [DataRequired()])
    # text = TextAreaField('Body')



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



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    widget = widgets.TableWidget()
    # widget = MyTableWidget()
    option_widget = widgets.CheckboxInput()


class SourcesForm(Form):
    """docstring for SourcesForm"""

    follow_sources = MultiCheckboxField('Subs')

    # def __init__(self, sources):
    #     super(SourcesForm, self).__init__()
    #     print('assigning sources ({}) to choices'.format(type(sources)))
    #     self.follow_sources.choices = sources

    # subs = build_sources()
    # wiki_subs('music', 'musicsubreddits')

    # follow_subs = SelectField('subs', choices=subs)



# class SourcesForm(Form):
#     Select Subreddits to follow
#     follow_subs = SelectField('subreddits')

    
