from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
album_review = Table('album_review', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('artist', VARCHAR(length=120)),
    Column('album', VARCHAR(length=120)),
    Column('photo', VARCHAR),
    Column('content', VARCHAR),
    Column('pub_date', DATETIME),
    Column('author_id', INTEGER),
)

album_review = Table('album_review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist', String(length=120)),
    Column('album', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('author', Integer),
)

article = Table('article', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=120)),
    Column('photo', VARCHAR),
    Column('content', VARCHAR),
    Column('pub_date', DATETIME),
    Column('featured', BOOLEAN),
    Column('author_id', INTEGER),
)

article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120), primary_key=True, nullable=False),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('featured', Boolean),
    Column('author', Integer),
)

track_review = Table('track_review', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('artist', VARCHAR(length=120)),
    Column('album', VARCHAR(length=120)),
    Column('name', VARCHAR(length=120)),
    Column('photo', VARCHAR),
    Column('content', VARCHAR),
    Column('pub_date', DATETIME),
    Column('author_id', INTEGER),
)

track_review = Table('track_review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist', String(length=120)),
    Column('album', String(length=120)),
    Column('name', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('author', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['album_review'].columns['author_id'].drop()
    post_meta.tables['album_review'].columns['author'].create()
    pre_meta.tables['article'].columns['author_id'].drop()
    post_meta.tables['article'].columns['author'].create()
    pre_meta.tables['track_review'].columns['author_id'].drop()
    post_meta.tables['track_review'].columns['author'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['album_review'].columns['author_id'].create()
    post_meta.tables['album_review'].columns['author'].drop()
    pre_meta.tables['article'].columns['author_id'].create()
    post_meta.tables['article'].columns['author'].drop()
    pre_meta.tables['track_review'].columns['author_id'].create()
    post_meta.tables['track_review'].columns['author'].drop()
