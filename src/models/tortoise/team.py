from tortoise import fields, models


class Team(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=120, description="小隊名稱")
    token = fields.CharField(max_length=4, unique=True, null=True, description="小隊權杖")

    def __str__(self):
        return f"第{self.id}小隊-{self.name}"
