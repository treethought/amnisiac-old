# project/server/sc/views.py


#################
#### imports ####
#################

from flask import Blueprint, request, session, jsonify, render_template
from project.server.sc.forms import ScSearchForm
from project.server.sc import api
################
#### config ####
################

sc_blueprint = Blueprint('sc', __name__,)


################
#### routes ####
################


@sc_blueprint.route('/load_tracks')
def load_tracks():
    queries = session['query'].split(',')
    embeds = []
    for q in [q for q in queries if len(q) > 1]:
        print('getting artist -- {}'.format(q))
        artist = api.get_user(q.strip())
        i = 0
        for track in api.user_tracks(artist):
            if i > 10:
                break
            print('getting -- {}'.format(track.title))
            html = api.embed_info(track.permalink_url)
            embeds.append(html)
            i += 1
    return jsonify(embeds)


@sc_blueprint.route('/sc_results', methods=['POST'])
def results():
    form = ScSearchForm(request.form)
    query = form.search_bar.data
    session['query'] = query
    queries = query.split(',')
    return render_template('main/sc_results.html', queries=queries)


@sc_blueprint.route('/sc_autocomplete', methods=['GET'])
def autocomplete():
    results = []
    term = request.args.get('q')
    for user in api.search_user(term):
        if term.lower() in user.username.lower():
            results.append(user.username)

    return jsonify(results=results)