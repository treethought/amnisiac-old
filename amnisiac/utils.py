# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


class AdminModelView(ModelView):

    def is_accessible(self):
        return getattr(current_user, 'admin', False)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.login', next=request.url))
