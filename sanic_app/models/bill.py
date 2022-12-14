from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_queryset_creator, pydantic_model_creator


class Bill(Model):
    id = fields.IntField(pk=True)
    balance: int = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = fields.ForeignKeyField("models.User", related_name="score_user")

    class Meta:
        table: str = "bill"


BillQueryCreate = pydantic_queryset_creator(Bill, name="BillQueryCreate")
