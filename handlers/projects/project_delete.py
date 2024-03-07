from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class DeleteProject:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def delete(self):
        try:
            proj_id = self.data['proj_id']
            dept_id = self.data['dept_id']

            delete_query = f'''

                DELETE FROM task_user_association
                USING tasks t
                WHERE t.task_id = task_user_association.task_id
                AND t.department_id = :dept_id
                AND t.project_id = :proj_id
                AND task_user_association.project_id = :proj_id;

                DELETE FROM tasks
                WHERE department_id = :dept_id
                AND project_id = :proj_id;

                DELETE FROM task_types
                WHERE department_id = :dept_id
                AND project_id = :proj_id;

                DELETE FROM project_user_association    
                WHERE project_id = :proj_id
                AND department_id = :dept_id;

                DELETE FROM projects_info
                WHERE project_id = :proj_id AND department_id = :dept_id;
                
            '''
            db.session.execute(text(delete_query), {
                    "proj_id": proj_id,
                    "dept_id": dept_id,
                })
            db.session.commit()

            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
