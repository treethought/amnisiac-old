# project/server/user/views.py


#################
#### imports ####
#################

from flask import Blueprint, request, session, jsonify, render_template
from project.server.main.forms import SearchForm
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
    print('FROM SESSION!')
    print(session['query'])
    print(str(request.args))
    queries = session['query'].split(',')
    # query = request.args.get('artists')
    embeds = []
    for q in [q for q in queries if len(q) > 1]:
        print('getting artist -- {}'.format(q))
        artist = api.get_user(q.strip())
        print('username is {}'.format(artist.username))
        i = 0
        for track in api.user_tracks(artist):
            if i > 10:
                break
            print('getting info for track')
            print(track.title)
            html = api.embed_info(track.permalink_url)
            embeds.append(html)
            i += 1
            print(i)
            # yield(html)
    return jsonify(embeds)


@sc_blueprint.route('/sc_results', methods=['POST'])
def results():
    print('in sc_results')
    form = SearchForm(request.form)
    query = form.search_field.data
    session['query'] = query
    queries = query.split(',')
    return render_template('main/sc_results.html', queries=queries)


@sc_blueprint.route('/sc_autocomplete', methods=['GET'])
def autocomplete():
    print(request)
    print('Searching')
    results = []
    term = request.args.get('q')
    print('**********{}*********'.format(term))
    for user in api.search_user(term):
        print(user.username)
        if term.lower() in user.username.lower():
            results.append(user.username)

    return jsonify(results=results)