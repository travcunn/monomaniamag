from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artist_review = Table('artist_review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('pub_date', DateTime),
    Column('author_id', Integer),
    Column('page_title', String),
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
    Column('page_title', String),
    Column('url', String),
)

article = Table('article', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=120)),
    Column('photo', VARCHAR),
    Column('content', VARCHAR),
    Column('pub_date', DATETIME),
    Column('featured', BOOLEAN),
    Column('author_id', INTEGER),
    Column('url', VARCHAR),
)

article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('page_title', String(length=120)),
    Column('photo', String),
    Column('content', String),
    Column('preview', String),
    Column('pub_date', DateTime),
    Column('featured', Boolean),
    Column('author_id', Integer),
    Column('url', String),
)

video = Table('video', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR),
    Column('thumbnail', VARCHAR),
    Column('pub_date', DATETIME),
    Column('url', VARCHAR),
)

video = Table('video', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('category', Integer),
    Column('pub_date', DateTime),
    Column('youtube_id', String),
    Column('content', String),
    Column('author_id', Integer),
    Column('url', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_review'].create()
    post_meta.tables['track_review'].columns['page_title'].create()
    pre_meta.tables['article'].columns['title'].drop()
    post_meta.tables['article'].columns['page_title'].create()
    post_meta.tables['article'].columns['preview'].create()
    pre_meta.tables['video'].columns['thumbnail'].drop()
    post_meta.tables['video'].columns['author_id'].create()
    post_meta.tables['video'].columns['category'].create()
    post_meta.tables['video'].columns['content'].create()
    post_meta.tables['video'].columns['youtube_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_review'].drop()
    post_meta.tables['track_review'].columns['page_title'].drop()
    pre_meta.tables['article'].columns['title'].create()
    post_meta.tables['article'].columns['page_title'].drop()
    post_meta.tables['article'].columns['preview'].drop()
    pre_meta.tables['video'].columns['thumbnail'].create()
    post_meta.tables['video'].columns['author_id'].drop()
    post_meta.tables['video'].columns['category'].drop()
    post_meta.tables['video'].columns['content'].drop()
    post_meta.tables['video'].columns['youtube_id'].drop()
