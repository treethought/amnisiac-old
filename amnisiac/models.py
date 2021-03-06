# amisiac/models.py
import datetime
from flask_restful import fields

from amnisiac.extensions import db, bcrypt


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


associations = db.Table('feeds',
                        db.Column('feed_id', db.Integer,
                                  db.ForeignKey('feed.id')),
                        db.Column('user_id', db.Integer,
                                  db.ForeignKey('user.id')),
                        db.Column('item_id', db.Integer,
                                  db.ForeignKey('item.id'))
                        )


class User(db.Model):

    # __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # email = db.Column(db.String(255), unique=False, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    # sources = db.relationship('Source', lazy='dynamic')
    feeds = db.relationship('Feed', secondary=associations,
                            backref=db.backref('subscribed_users', lazy='dynamic'))

    favorites = db.relationship('Item', secondary=associations,
                                backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, email=None, admin=False):
        # self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.String(), unique=True, nullable=False)
    domain = db.Column(db.String(), unique=False, nullable=True)
    items = db.relationship('Item', secondary=associations,
                            backref=db.backref('feeds', lazy='dynamic'))

    def __repr__(self):
        return '<Feed:{} from {}>'.format(self.name, self.domain)


# TODO: track_id as primary key? must be string
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(), unique=True, nullable=False)
    raw_title = db.Column(db.String(), unique=False, nullable=True)
    title = db.Column(db.String(), unique=False, nullable=True)
    artist = db.Column(db.String(), unique=False, nullable=True)
    url = db.Column(db.String(), unique=False, nullable=True)
    domain = db.Column(db.String(), unique=False, nullable=True)
    date_published = db.Column(db.DateTime, nullable=True)
    date_saved = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(), unique=False, nullable=False)
    subreddit = db.Column(db.String(), unique=False, nullable=True)
    r_created_utc = db.Column(db.Integer(), nullable=True)

    # for sc 
    uri = db.Column(db.String(), unique=False, nullable=True)
    duration = db.Column(db.Integer(), unique=False, nullable=True)
    embeddable_by = db.Column(db.String(), unique=False, nullable=True)
    artwork_url = db.Column(db.String(), unique=False, nullable=True)
    streamable = db.Column(db.String(), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, unique=False, nullable=True)
    genre = db.Column(db.String(), unique=False, nullable=True)
    waveform_url = db.Column(db.String(), unique=False, nullable=True)
    stream_url = db.Column(db.String(), unique=False, nullable=True)

    pub_date = db.Column(db.Integer(), nullable=True) # for sorting posts


    def __init__(self, track_id, source, subreddit=None, **kwargs):
        super(Item, self).__init__(**kwargs)

        self.track_id = track_id
        self.source = source
        self.subreddit = subreddit
        self.date_saved = datetime.datetime.now()


    def parse_raw_title(self):
        pass

    def __repr__(self):
        return '<Item:{} from {}'.format(self.raw_title, self.feeds)


# Fields used to structure API responses using marshal_with
item_fields = {
    # 'id': fields.Integer,
    'track_id': fields.String,
    'raw_title': fields.String,
    'title': fields.String,
    'artist': fields.String,
    'url': fields.String,
    'domain': fields.String,
    # 'date_published': fields.DateTime,
    'date_saved': fields.DateTime,
    'pub_date': fields.Integer,
    'source': fields.String,
    'subreddit': fields.String,
    # for sc
    'uri': fields.String,
    'duration': fields.String,
    'embeddable_by': fields.String,
    'artwork_url': fields.String,
    'streamable': fields.String,
    'created_at': fields.String,
    'genre': fields.String,
    'waveform_url': fields.String,
    'stream_url': fields.String
}

feed_fields = {
    'name': fields.String,
    'url': fields.String,
    'domain': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'feeds': fields.List(fields.Nested(feed_fields)),
    'favorites': fields.List(fields.Nested(item_fields))
}
