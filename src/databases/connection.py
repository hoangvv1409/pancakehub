from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session


def db_engine(connection_url, **options):
    return create_engine(connection_url, pool_size=100)


def bind_session(engine, custom_session=None):
    session = custom_session or scoped_session(
        sessionmaker(autocommit=False)
    )
    session.configure(bind=engine)

    return session


@contextmanager
def session_scope(scope=None, auto_commit=True):
    """Provide a transactional scope around a series of operations."""
    session = scope
    try:
        yield session
        if auto_commit:
            session.commit()
    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
