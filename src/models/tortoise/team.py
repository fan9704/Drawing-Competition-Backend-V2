from tortoise import fields, models

class Team(models.Model):
    """
    小隊 Model
    """
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=120)
    token = fields.CharField(max_length=4,unique=True,null=True)