from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
    Column('thumbnail', String),
    Column('pub_date', DateTime),
    Column('youtube_id', String),
    Column('content', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['video'].columns['url'].drop()
    post_meta.tables['video'].columns['content'].create()
    post_meta.tables['video'].columns['youtube_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['video'].columns['url'].create()
    post_meta.tables['video'].columns['content'].drop()
    post_meta.tables['video'].columns['youtube_id'].drop()
