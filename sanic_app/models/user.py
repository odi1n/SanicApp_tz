from uuid import uuid4

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from sanic_app.models.bill import Bill


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    confirmation = fields.UUIDField(default=uuid4)

    bills: fields.ReverseRelation['Bill']

    class Meta:
        table: str = "user"

    def __str__(self):
        return f"User {self.id}: {self.username}"

    @property
    def get_scopes(self):
        scopes = ['user']
        if self.is_superuser:
            scopes.append('admin')
        return scopes

    def to_dict(self):
        return {"user_id": self.id, "username": self.username, "scopes": self.get_scopes}


UserModelCreate = pydantic_model_creator(User, name="UserModelCreate",
                                         exclude=('password', 'is_superuser', 'bills'))
UserModelCreateExl = pydantic_model_creator(User, name="UserModelCreateExl", exclude_readonly=True, )
