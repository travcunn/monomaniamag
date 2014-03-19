from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    album_reviews = db.relationship('AlbumReview', backref='author',
                                    lazy='dynamic')
    artist_reviews = db.relationship('ArtistReview', backref='author',
                                    lazy='dynamic')
    track_reviews = db.relationship('TrackReview', backref='author',
                                    lazy='dynamic')
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    videos = db.relationship('Video', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.realname)


class AlbumReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120))
    album = db.Column(db.String(120))
    photo = db.Column(db.String)
    content = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_title = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return '<AlbumReview %r>' % (self.album)


class TrackReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120))
    album = db.Column(db.String(120))
    name = db.Column(db.String(120))
    photo = db.Column(db.String)
    content = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_title = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return '<TrackReview %r>' % (self.name)


class ArtistReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120))
    photo = db.Column(db.String)
    content = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_title = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return '<ArtistReview %r>' % (self.artist)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.String(120), unique=True)
    photo = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    featured = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String)

    def __repr__(self):
        return '<Article %r>' % (self.page_title)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)
    youtube_id = db.Column(db.String)
    content = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String)

    def __repr__(self):
        return '<Video %r>' % (self.title)
