import re

WORD_VAL = re.compile('^[\w\s\-]+$')
TASK_VAL = re.compile('^[\w\s\-\.,]+$')
WALL_VAL = re.compile('^[\w\s\-\.,!_\(\)\/\?:]+$')
