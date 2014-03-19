from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import BooleanField, RadioField, TextAreaField, TextField
from wtforms.validators import Required

from app import db
from models import User


class AlbumReviewForm(Form):
    artist = TextField('Artist', validators=[Required()])
    album = TextField('Album', validators=[Required()])
    upload = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    content = TextAreaField('Content', validators=[Required()])


class AlbumReviewFormEdit(Form):
    artist = TextField('Artist', validators=[Required()])
    album = TextField('Album', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])


class AlbumReviewFormDelete(Form):
    pass


class TrackReviewForm(Form):
    artist = TextField('Artist', validators=[Required()])
    album = TextField('Album', validators=[Required()])
    name = TextField('Name', validators=[Required()])
    upload = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    content = TextAreaField('Content', validators=[Required()])


class TrackReviewFormEdit(Form):
    artist = TextField('Artist', validators=[Required()])
    album = TextField('Album', validators=[Required()])
    name = TextField('Name', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])


class TrackReviewFormDelete(Form):
    pass


class ArtistReviewForm(Form):
    artist = TextField('Artist', validators=[Required()])
    upload = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    content = TextAreaField('Content', validators=[Required()])


class ArtistReviewFormEdit(Form):
    artist = TextField('Artist', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])


class ArtistReviewFormDelete(Form):
    pass


class NewsForm(Form):
    title = TextField('Title', validators=[Required()])
    preview = TextField('Preview', validators=[Required()])
    featured = BooleanField('Featured')
    upload = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    content = TextAreaField('Content', validators=[Required()])


class NewsFormEdit(Form):
    title = TextField('Title', validators=[Required()])
    preview = TextField('Preview', validators=[Required()])
    featured = BooleanField('Featured')
    content = TextAreaField('Content', validators=[Required()])

class NewsFormDelete(Form):
    pass


class VideoForm(Form):
    title = TextField('Title', validators=[Required()])
    category = RadioField('Category', choices=[(1, 'Music Video'),
                                               (2, 'Interview'),
                                               (3, 'Writer Video')],
                          validators=[Required()])
    youtube_id = TextField('Youtube Video ID', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])


class LoginValidator(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    @property
    def is_valid(self):
        user = self.lookup_user
        if user is None:
            return False

        if user.password != self.__password:
            return False

        return True

    @property
    def lookup_user(self):
        return db.session.query(User).filter_by(email=self.__username).first()
