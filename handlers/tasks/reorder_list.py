from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class ReorderStages:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def reorder(self):
        try:            
            update_query = f'''
                update projects_info set task_order = :orderlist where project_id = :proj_id and department_id =:dept_id
            '''
            db.session.execute(
                text(update_query),
                {
                    "orderlist": self.data['columns'],
                    "proj_id":self.data['proj_id'],
                    "dept_id":self.data['dept_id']
                })
            db.session.commit()

            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}

    def update_col_name(self):
        try:            
            update_query = f'''
                update task_types set name = :name where project_id=:proj_id and department_id =:dept_id and type_id = :type_id
            '''
            db.session.execute(
                text(update_query),
                {
                    "name": self.data['name'],
                    "proj_id":self.data['proj_id'],
                    "type_id":self.data['type_id'],
                    "dept_id":self.data['dept_id']
                })
            db.session.commit()

            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}