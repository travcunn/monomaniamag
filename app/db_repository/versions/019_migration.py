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
    Column('content', VARCHAR),
    Column('youtube_id', VARCHAR),
    Column('category', INTEGER),
    Column('url', VARCHAR),
    Column('author_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['video'].columns['thumbnail'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['video'].columns['thumbnail'].create()
