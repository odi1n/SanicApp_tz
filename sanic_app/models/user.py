from uuid import uuid4

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    confirmation = fields.UUIDField(default=uuid4)

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


UserPydanticOut = pydantic_model_creator(User, name="UserOut",
                                         exclude=('password', 'confirmation', 'is_superuser'))
UserPydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, )
