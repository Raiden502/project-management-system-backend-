from datetime import datetime
from typing import List
from time import sleep

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
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  # Remove microseconds
    temp={}
    for item in type:
        temp[item] = f'{config.get(item)}_{timestamp}'
        sleep(delay)
    
    return temp