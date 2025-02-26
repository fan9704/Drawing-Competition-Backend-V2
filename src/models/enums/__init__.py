from enum import Enum


class StatusEnum(str, Enum):
    todo = 'todo'
    doing = 'doing'
    success = 'success'
    fail = 'fail'


class DifficultyEnum(str, Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'
