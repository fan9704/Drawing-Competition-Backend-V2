from tortoise import fields, models, timezone


class Submission(models.Model):
    """
    提交紀錄 Model
    """
    @staticmethod
    def validate_range(value: int) -> int:
        """
        驗證數值必須為 0 ~ 100 之間的整數。
        """
        if not isinstance(value, int) or value < 0 or value > 100:
            raise ValueError("Value must be an integer between 0 and 100.")
        return value

    # 狀態選項
    STATUS_OPTIONS = [
        ("todo", "todo"),
        ("doing", "doing"),
        ("fail", "fail"),
        ("success", "success"),
    ]
    id = fields.IntField(pk=True)
    # 程式碼
    code = fields.TextField(default="", verbose_name="程式碼")
    # 提交狀態
    status = fields.CharField(
        max_length=255, choices=STATUS_OPTIONS, default="todo", verbose_name="狀態"
    )
    # 評分相關
    score = fields.IntField(
        default=0, validators=[validate_range], verbose_name="分數"
    )
    # 吻合度
    fitness = fields.IntField(
        default=0, validators=[validate_range], verbose_name="吻合度"
    )
    # 程式字數
    word_count = fields.IntField(default=0, verbose_name="單字數")
    # 執行時間（使用 TimeDeltaField 來記錄時間間隔）
    execute_time = fields.TimeDeltaField(null=True, description="執行時間")
    # 輸出相關
    stdout = fields.TextField(default="", verbose_name="標準輸出")
    stderr = fields.TextField(default="", verbose_name="標準錯誤")
    # 資訊相關
    team = fields.ForeignKeyField("models.Team", on_delete=fields.CASCADE, verbose_name="隊伍")
    time = fields.DatetimeField(default=timezone.now, verbose_name="時間")
    challenge = fields.ForeignKeyField(
        "models.Challenge",related_name="submission", on_delete=fields.CASCADE, verbose_name="挑戰"
    )
    round = fields.ForeignKeyField("models.Round", on_delete=fields.CASCADE, verbose_name="回合")
    draw_image_url = fields.TextField(default="", verbose_name="繪圖圖片連結")

    def __str__(self):
        return f"{self.team}-{self.time.time()}-{self.round}-吻合度:{self.fitness}"