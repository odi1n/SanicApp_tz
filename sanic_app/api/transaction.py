from sanic import Blueprint, HTTPResponse
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user

from sanic_app.models import TransactionQueryCreate, Transaction, User

transaction = Blueprint("transaction", url_prefix="/transaction", strict_slashes=True)


@transaction.get('/', strict_slashes=False)
@openapi.summary("Get transactions")
@openapi.description("Get all transactions")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, TransactionQueryCreate, description="Model Transaction")
@protected()
@inject_user()
async def get_transaction(request, user: User):
    transaction = await TransactionQueryCreate.from_queryset(Transaction.filter(bill__user_id=user.id).all())
    return HTTPResponse(body=transaction.json(), content_type="application/json")
