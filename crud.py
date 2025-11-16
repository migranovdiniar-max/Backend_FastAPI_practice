import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Post, Profile, User
from sqlalchemy.orm import joinedload, selectinload


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None =  result.scalar_one_or_none()
    user = await session.scalar(stmt)
    print("found user:", username, user)
    return user


async def create_user_profile(session: AsyncSession, user_id: int, 
                              first_name: str | None = None, last_name: str | None = None) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.profile))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    
    for user in users:
        print("user:", user)
        print(" profile:", user.profile.first_name)


async def create_posts(session: AsyncSession, 
                       user_id: int, 
                       *posts_titles: str) -> list[Post]:
    posts = [
        Post(titlee=title, user_id=user_id)
        for title in posts_titles
    ]

    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print('**' * 10)
        print("user:", user)
        for post in user.posts:
            print(" post:", post)


async def get_users_with_posts_and_profiles(session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(joinedload(User.profile))
        .options(selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print('**' * 10)
        print("user:", user, user.profile and user.profile.first_name)
        for post in user.posts:
            print(" post:", post)


async def get_posts_with_authors(session: AsyncSession) -> list[Post]:
    stmt = (
        select(Post)
        .options(joinedload(Post.user))
        .order_by(Post.id)
    )
    posts = await session.scalars(stmt)
    for post in posts:
        print('**' * 10)
        print("post:", post)
        print(" author:", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession) -> list[Profile]:
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == 'john')
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)
    for profile in profiles:
        print('**' * 10)
        print("profile:", profile.first_name, profile.user)
        print(" user:", profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="sam")
        user_sam = await get_user_by_username(session=session, username="sam")
        user_john = await get_user_by_username(session=session, username="john")
        # # await get_user_by_username(session=session, username="alice")

        # await create_user_profile(session=session, user_id=user_john.id, 
        #                           first_name="John", last_name="Smith")
        
        # await create_user_profile(session=session, user_id=user_sam.id, 
        #                           first_name="Sam", last_name="Winchester")

        # await show_users_with_profiles(session=session)
        # await create_posts(session, 
        #                    user_john.id,
        #                    "Sqlalchemy intro",
        #                    "sqlalchemy advanced")
        
        # await create_posts(session, 
        #                    user_sam.id,
        #                    "FastAPI intro",
        #                    "FastAPI advanced",
        #                    "FastAPI more")

        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())