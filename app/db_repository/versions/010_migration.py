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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_review'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_review'].drop()
