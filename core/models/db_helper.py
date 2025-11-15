from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    AsyncSession, 
                                    async_sessionmaker,
                                    async_scoped_session)
from core.config import settings
from asyncio import current_task


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo)

        # async_sessionmaker uses sqlalchemy Session arg names (autoflush, expire_on_commit)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )


    def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )

        return session
    

    async def session_dependency(self):
        # FastAPI dependency: yield an async session
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DataBaseHelper(url=settings.db_url, echo=settings.db_echo)