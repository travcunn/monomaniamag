import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))

ALBUM_REVIEWS_PER_PAGE = 9
ARTIST_REVIEWS_PER_PAGE = 9
TRACK_REVIEWS_PER_PAGE = 9

CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'

