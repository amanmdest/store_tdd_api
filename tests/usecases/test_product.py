from uuid import UUID
import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


@pytest.mark.asyncio
async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(
            id=UUID("f8827cf6-d5cf-4dfd-8790-fc83aec54315")
        )

    assert (
        err.value.message
        == "Product not found with filter: f8827cf6-d5cf-4dfd-8790-fc83aec54315"
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, list)
    assert len(result) > 1


@pytest.mark.asyncio
async def test_usecases_update_should_return_success(
    product_up, product_inserted
):
    product_up.price = "7.500"
    result = await product_usecase.update(
        id=product_inserted.id, body=product_up
    )

    assert isinstance(result, ProductUpdateOut)


@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


@pytest.mark.asyncio
async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(
            id=UUID("f8827cf6-d5cf-4dfd-8790-fc83aec54315")
        )

    assert (
        err.value.message
        == "Product not found with filter: f8827cf6-d5cf-4dfd-8790-fc83aec54315"
    )
