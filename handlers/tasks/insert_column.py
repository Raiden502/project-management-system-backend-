from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class TaskTypeCreate:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewTaskType(self):
        try:
            ids = generate_uniqueId(type=['task_type'])
            task_query = f'''
                insert into task_types(type_id, project_id, department_id, name, created_by)
                values(:type_id, :proj_id, :dept_id, :name, :user_id)
            '''
            db.session.execute(
                text(task_query),
                {
                    "type_id":ids.get('task_type'),
                    "proj_id":self.data['proj_id'],
                    "dept_id":self.data['dept_id'],
                    "name":self.data["name"], 
                    "user_id":self.data["user_id"],
                })
            db.session.commit()

            order_list = f'''
                select task_order from projects_info where project_id = :proj_id
            '''
            result = db.session.execute(
                text(order_list),
                {
                    "proj_id":self.data['proj_id'],
                }).fetchone()
            
            update_query = f'''
                update projects_info set task_order = :orderlist where project_id = :proj_id
            '''

            list_data = list(result[0])
            list_data.append(ids.get('task_type'))
            db.session.execute(
                text(update_query),
                {
                    "orderlist":list_data,
                    "proj_id":self.data['proj_id'],
                })
            db.session.commit()

            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
                "data":{
                    "id":ids.get('task_type'),
                    "name":self.data["name"],
                    "taskIds":[] 
                }
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}
