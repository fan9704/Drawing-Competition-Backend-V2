from tortoise import fields, models


class Challenge(models.Model):
    DIFFICULTY_OPTIONS = [
        ("easy", "easy"),
        ("medium", "medium"),
        ("hard", "hard"),
    ]

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255, default="題目標題", description="題目標題")
    description = fields.TextField(description="題目描述")
    # 注意：Tortoise 沒有內建的 ImageField，你可以將圖片路徑以字串儲存，
    # 或使用其他套件處理檔案上傳
    image_url = fields.CharField(
        max_length=255, default="images/default.png", description="題目圖片"
    )
    difficulty = fields.CharField(
        max_length=255, choices=DIFFICULTY_OPTIONS, default="easy", description="難度"
    )
    round = fields.ForeignKeyField("models.Round",related_name="challenge_list", on_delete=fields.CASCADE, description="回合")
    is_valid = fields.BooleanField(default=True, description="是否有效")

    def __str__(self):
        return f"題目編號:{self.id}-標題；{self.title}-描述：{self.description}"
