from flask import g
import sqlalchemy as sqldb
from sqlalchemy.pool import SingletonThreadPool


# DATABASE = 'annotations.db'
DATABASE = 'sqlite:///annotations.db'


def parse_boolean(value):
    if type(value) is bool:
        return value
    elif type(value) is str:    
        value = value.lower()

        if value in ["true", "yes", "y", "1", "t"]:
            return True
        elif value in ["false", "no", "n", "0", "f"]:
            return False

    return False


class DBConnection:
    def __init__(self, _engine, _connection, _metadata):
        self.engine = _engine
        self.connection = _connection
        self.metadata = _metadata


def get_db() -> DBConnection:
    if getattr(g, '_db', None) is None:
        _engine = sqldb.create_engine(DATABASE, poolclass=SingletonThreadPool)
        _connection = _engine.connect()
        _metadata = sqldb.MetaData(_engine)
        _metadata.reflect()
        g._db = DBConnection(_engine, _connection, _metadata)
    return g._db


def get_global(key):
    db = get_db()
    globals = db.metadata.tables['globals']
    query = sqldb.select([globals]).where(globals.columns.key == key)
    result = db.connection.execute(query).one()
    return result['value']
