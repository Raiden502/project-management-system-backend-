from datetime import datetime
from typing import List
from time import sleep
import random
import string

def generate_uniqueId(type:List[str], delay = 0)->str:
    config = {
        'organization':'O',
        'user':'U',
        'group':'G',
        'group_user':'GU',
        'department':'D',
        'department_user':'DU',
        'project':'P',
        'project_user':'PU',
        'messages':'M',
        'task':'T',
        'task_type':'TT',
        'task_file':'TF',
        'task_users':'TU',
        'task_comment':'TC',
        'team':'TE',
        'team_user':'TEU',
        'file':'F'
    }
    temp={}
    for item in type:
        timestamp = str(datetime.now().timestamp()).replace('.', '') 
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        temp[item] = f'{config.get(item)}_{timestamp}{random_chars}'
    return temp