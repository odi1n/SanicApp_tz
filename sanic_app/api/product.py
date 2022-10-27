from sanic import Blueprint, exceptions
from sanic import Blueprint, exceptions
from sanic.response import HTTPResponse
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user
from tortoise import transactions
from tortoise.expressions import F

from sanic_app.models import Product, ProductPydanticOut, User, Score, Transaction, TransactionPydanticOut
from sanic_app.serializers import TransactionParams

product = Blueprint("product", url_prefix="/product", strict_slashes=True)


@product.get('/', strict_slashes=False)
@openapi.summary("Get  products")
@openapi.description("Get all products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, ProductPydanticOut, description="Product params")
@protected()
async def get_products(request):
    products = await ProductPydanticOut.from_queryset(Product.all())
    return HTTPResponse(body=products.json())


@product.post('/', strict_slashes=False)
@openapi.summary("Buy products")
@openapi.description("Buy products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.definition(body={'application/json': TransactionParams.schema()})
@protected()
@inject_user()
@validate(json=TransactionParams, body_argument="transaction_params")
async def buy_products(request, user: User, transaction_params: TransactionParams):
    score = await Score.filter(uid=transaction_params.score_id,
                               user__id=user.get('id')).first()
    if score is None:
        raise exceptions.NotFound("Incorrect score")
    if score.balance < transaction_params.amount:
        raise exceptions.NotFound("Not balance")

    product = await Product.filter(id=transaction_params.product_id).first()
    if product is None:
        raise exceptions.NotFound("Incorrect product")

    async with transactions.in_transaction():
        score.balance = F("balance") - transaction_params.amount
        await score.save(update_fields=['balance'])
        transaction = await Transaction.create(score=score,
                                               amount=transaction_params.amount,
                                               product=product)
    transaction = await TransactionPydanticOut.from_tortoise_orm(transaction)
    return HTTPResponse(body=transaction.json())
