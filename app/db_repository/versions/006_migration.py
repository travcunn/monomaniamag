from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
album_review = Table('album_review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist', String(length=120)),
    Column('album', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('author_id', Integer),
    Column('url', String),
)

article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('featured', Boolean),
    Column('author_id', Integer),
    Column('url', String),
)

track_review = Table('track_review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist', String(length=120)),
    Column('album', String(length=120)),
    Column('name', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('author_id', Integer),
    Column('url', String),
)

video = Table('video', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('thumbnail', String),
    Column('pub_date', DateTime),
    Column('url', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['album_review'].columns['url'].create()
    post_meta.tables['article'].columns['url'].create()
    post_meta.tables['track_review'].columns['url'].create()
    post_meta.tables['video'].columns['url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['album_review'].columns['url'].drop()
    post_meta.tables['article'].columns['url'].drop()
    post_meta.tables['track_review'].columns['url'].drop()
    post_meta.tables['video'].columns['url'].drop()
