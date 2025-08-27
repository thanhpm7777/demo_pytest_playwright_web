# core/db.py
from functools import lru_cache
from typing import Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL
from configs.settings import settings  # lưu ý import này

@lru_cache
def get_mysql_engine() -> Engine:
    url = URL.create(
        drivername="mysql+pymysql",
        username=settings.MYSQL_USER,       # có thể chứa @ : / ? #
        password=settings.MYSQL_PASSWORD,   # có thể chứa @ : / ? #
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DB,
    )
    return create_engine(url, pool_pre_ping=True, future=True)


def run_query(query: str, params: Optional[Dict] = None) -> List[Dict]:
    engine = get_mysql_engine()
    with engine.connect() as conn:
        res = conn.execute(text(query), params or {})
        return [dict(row._mapping) for row in res]


def execute(query: str, params: Optional[Dict] = None) -> int:
    engine = get_mysql_engine()
    with engine.begin() as conn:
        res = conn.execute(text(query), params or {})
        return getattr(res, "rowcount", 0)
