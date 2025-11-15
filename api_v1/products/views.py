from fastapi import APIRouter, Body, HTTPException, status, Depends
from .import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import product_by_id_dependency


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_helper.session_dependency),
                       ):
    return await crud.get_products(session=session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product: Product = Depends(product_by_id_dependency)):
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate = Body(...), 
                         session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_product(session=session, product_in=product_in)


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductUpdate = Body(...),
    product: Product = Depends(product_by_id_dependency),
    session: AsyncSession = Depends(db_helper.session_dependency
)):
    return await crud.update_product(session=session, product=product, 
                                     product_update=product_update)


@router.patch("/{product_id}/", response_model=Product)
async def update_product_partial(
    product_update: ProductUpdatePartial = Body(...),
    product: Product = Depends(product_by_id_dependency),
    session: AsyncSession = Depends(db_helper.session_dependency
)):
    return await crud.update_product(session=session, product=product, 
                                     product_update=product_update, partial=True)


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id_dependency),
    session: AsyncSession = Depends(db_helper.session_dependency
)):
    await crud.delete_product(session=session, product=product)
    return None