"""
Tortoise models.
"""

from tortoise import Model, fields
from src.models.tortoise.team import Team
from src.models.tortoise.round import Round
from src.models.tortoise.challenge import Challenge
from src.models.tortoise.submission import Submission

class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()