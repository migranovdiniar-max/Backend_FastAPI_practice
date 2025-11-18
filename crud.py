import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Post, Profile, User
from sqlalchemy.orm import joinedload, selectinload

from core.models.order import Order
from core.models.order_product_association import OrderProductAssociation
from core.models.product import Product


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


async def main_relations(session: AsyncSession):
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


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.products))
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    for order in orders:
        print('**' * 10)
        print("order:", order)
        for product in order.products:
            print(" product:", product)


async def create_orders_and_products(session: AsyncSession) -> None:
    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")

    mouse = await create_product(session=session,
                                 name="Mouse",
                                description="Wireless mouse",
                                price=25)
    keyboard = await create_product(session=session,
                                    name="Keyboard",
                                    description="Mechanical keyboard",
                                    price=75)
    monitor = await create_product(session=session,
                                   name="Monitor",
                                   description="4K monitor",
                                   price=300)
    
    order_one = await session.scalar(select(Order)
                                     .where(Order.id == order_one.id)
                                     .options(
                                         selectinload(Order.products)
                                     ))
    order_promo = await session.scalar(select(Order)
                                       .where(Order.id == order_promo.id)
                                        .options(
                                             selectinload(Order.products)
                                        ))
    
    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(monitor)

    await session.commit()


async def create_order(session: AsyncSession, promocode: str | None = None) -> None:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()

    return order


async def create_product(session: AsyncSession, 
                         name: str,
                         description: str,
                         price: int) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price)
    session.add(product)
    await session.commit() 
    return product


async def demo_get_orders_with_posducts_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products: # type: ignore #type: Product
            print('-', product.id, product.name, product.price)


async def get_orders_with_posducts_assoc(session: AsyncSession):
    stmt = (
        select(Order)
        .options(selectinload(Order.products_details).joinedload(OrderProductAssociation.product))
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_posducts_through_assoc(session: AsyncSession):
    orders = await get_orders_with_posducts_assoc(session)

    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for order_product_detais in order.products_details:
            print('-', order_product_detais.product.name, 
                  order_product_detais.product.price, 
                  order_product_detais.count)    


async def demo_m2m(session: AsyncSession):
    # create_orders_and_products(session=session)
    # await demo_get_orders_with_posducts_through_assoc(session)
    pass


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)
        

if __name__ == "__main__":
    asyncio.run(main())