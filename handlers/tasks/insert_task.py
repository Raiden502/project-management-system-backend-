from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class TaskCreate:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewTask(self):
        try:
            ids = generate_uniqueId(type=['task'])
            task_query = f'''
                insert into tasks (task_id, type_id, project_id, department_id, name, created_by, priority)
                values(:task_id, :type_id, :proj_id,:dept_id, :name, :user_id, :priority);
            '''
            with db.session() as session:
                session.execute(
                    text(task_query),
                    {
                        "task_id":ids.get('task'),
                        "type_id":self.data['type_id'],
                        "proj_id":self.data['proj_id'],
                        "dept_id":self.data['dept_id'],
                        "name":self.data["name"], 
                        "user_id":self.data["user_id"],
                        "priority": self.data['priority'],
                    })
                session.commit()
            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
                "data":{
                    "id":ids.get('task'),
                    "name":self.data["name"], 
                    "priority": self.data['priority'],
                    "status":self.data['type_id'],
                    "type_id":self.data['type_id'],
                }
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}
        
    def delete_task(self):
        try:
            task_query = f'''
                delete from tasks where project_id  =:proj_id and department_id =:dept_id and task_id =:task_id
            '''
            with db.session() as session:
                session.execute(
                    text(task_query),
                    {
                        "task_id": self.data['taskId'],
                        "proj_id":self.data['proj_id'],
                        "dept_id":self.data['dept_id'],
                    })
                session.commit()
            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}