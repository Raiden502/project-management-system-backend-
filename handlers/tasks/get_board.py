from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class BoardDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_board_details(self):
        try:
            task_query = f''' 
                select 
                    t.task_id as id, 
                    t.name,
                    t.description,
                    t.due_date,
                    t.labels, 
                    t.priority, 
                    ty.name as status,
                    CASE 
                        WHEN u.user_id IS NOT NULL 
                        THEN json_build_object('id', u.user_id, 'name', u.user_name, 'avatarUrl', u.avatar)
                        ELSE NULL
                    END AS reporter,
                    ARRAY[]::json[] as comments, 
                    ARRAY[]::json[] as assignee, 
                    array[]::text[] as attachments  
                from tasks t
                left join task_types ty on t.type_id=ty.type_id
                left join user_info u on t.reporter = u.user_id
                where t.project_id = :project_id and t.department_id = :department_id
                group by id, t.name, t.description, t.due_date, t.labels,  t.priority, status,  u.user_id
            '''    
        
            task_result = dictfetchall(db.session.execute(
                    text(task_query), {"department_id":self.data['department_id'],"project_id":self.data['project_id'] }))
                
            order_query = f'''
                select task_order from projects_info where project_id = :project_id and department_id = :department_id
            '''

            order_result = db.session.execute(
                    text(order_query), {"department_id":self.data['department_id'],"project_id":self.data['project_id'] }).fetchone()
            
            column_query = f'''
                select 
                    ty.type_id as id,
                    ty.name,
                    array_agg(t.task_id) FILTER (WHERE t.task_id IS NOT NULL) AS "taskIds"
                from task_types ty
                left join tasks t on t.type_id = ty.type_id
                where ty.project_id = :project_id and ty.department_id = :department_id
                group by id, ty.name 
            '''

            column_result = dictfetchall(db.session.execute(
                    text(column_query), {"department_id":self.data['department_id'],"project_id":self.data['project_id'] }))
            
            print(self.data)
            return {
                "status": True,
                "message": "query successful",
                "errorcode": 0,
                "data": {
                    "tasks":task_result if task_result else [],
                    "columns":column_result if column_result else [],
                    "ordered":order_result[0] if order_result else [],
                }
            }

        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": {
                        "tasks":[],
                        "columns": [],
                        "ordered": [],
                    }
                }
