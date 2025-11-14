from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            auto_flush=False,
            auto_commit=False,
            expire_on_commit=False,
        )


db_helper = DataBaseHelper(url=settings.db_url, echo=settings.db_echo)