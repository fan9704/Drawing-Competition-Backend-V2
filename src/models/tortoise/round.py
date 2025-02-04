from tortoise import fields, models

class Round(models.Model):
    """
    回合 Model
    """
    id = fields.IntField(pk=True)
    start_time = fields.DatetimeField(null=False, description="開始時間")
    end_time = fields.DatetimeField(null=False, description="結束時間")
    is_valid = fields.BooleanField(default=True, description="是否有效")

    def __str__(self) -> str:
        return f"回合:{self.id}"