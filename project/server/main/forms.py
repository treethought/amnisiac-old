# project/server/main/forms

from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired
from project.server.scrapers.reddit_links import wiki_subs



class PostForm(Form):
    """Add new subreddit"""

    subreddit = TextField('Subreddit', [DataRequired()])
    # text = TextAreaField('Body')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
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

    
