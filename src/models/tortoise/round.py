from tortoise import fields, models
import pytz

tz = pytz.timezone("Asia/Taipei")

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

    def get_local_start_time(self):
        return self.start_time.replace(tzinfo=pytz.utc).astimezone(tz)

    def get_local_end_time(self):
        return self.end_time.replace(tzinfo=pytz.utc).astimezone(tz)