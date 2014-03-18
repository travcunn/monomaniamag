from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
article = Table('article', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=120)),
    Column('photo', VARCHAR),
    Column('content', VARCHAR),
    Column('pub_date', DATETIME),
    Column('featured', BOOLEAN),
    Column('author_id', INTEGER),
    Column('url', VARCHAR),
    Column('preview', VARCHAR),
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].columns['title'].drop()
    post_meta.tables['article'].columns['page_title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].columns['title'].create()
    post_meta.tables['article'].columns['page_title'].drop()
