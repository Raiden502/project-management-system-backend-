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
                    t.start_date,
                    t.due_date,
                    t.labels, 
                    t.priority, 
                    ty.name as status,
                    t.reporter,
                    COALESCE(
                        array_agg(
                            json_build_object('id', c.comment_id, 'name', cu.user_name, 'message', c.message, 'message_type',c.message_type, 'avatar', cu.avatar)) 
                        FILTER (WHERE c.comment_id IS NOT NULL),
                        ARRAY[]::JSON[]) AS comments,
                    COALESCE(array_agg(tu.user_id) FILTER (WHERE tu.user_id IS NOT NULL), ARRAY[]::VARCHAR[]) AS users,
                    COALESCE(array_agg(tu.team_id) FILTER (WHERE tu.team_id IS NOT NULL), ARRAY[]::VARCHAR[]) AS teams,
                    COALESCE(array_agg(
                            json_build_object('id', tf.relation_id, 'file', tf.file_src)) 
                        FILTER (WHERE  tf.relation_id IS NOT NULL),
                        ARRAY[]::JSON[]) AS attachments
                from tasks t
                left join task_types ty on t.type_id=ty.type_id
                left join task_user_association tu on tu.task_id = t.task_id
                left join comments c on c.task_id = t.task_id
                left join user_info cu on cu.user_id = c.user_id
                left join task_files_associaton tf on tf.task_id = t.task_id 
                where t.project_id = :project_id and t.department_id = :department_id
                group by id, t.name, t.description, t.due_date, t.labels,  t.priority, status,  t.reporter
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
                    COALESCE(array_agg(t.task_id) FILTER (WHERE t.task_id IS NOT NULL), ARRAY[]::VARCHAR[]) AS "taskIds"
                from task_types ty
                left join tasks t on t.type_id = ty.type_id
                where ty.project_id = :project_id and ty.department_id = :department_id 
                group by id, ty.name 
            '''

            column_result = dictfetchall(db.session.execute(
                    text(column_query), {"department_id":self.data['department_id'],"project_id":self.data['project_id'] }))
            
            print("task_result \n", self.data)
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
        
    def get_project_users(self):
        try:
            task_query = f''' 
                select 
                    array_agg(json_build_object('id', u.user_id, 'name', u.user_name, 'avatar', u.avatar, 'role', u.role)) FILTER (WHERE u.user_id IS NOT NULL) AS userlist,
                    array_agg(json_build_object('id', t.team_id, 'name', t.name, 'avatar', t.avatar)) FILTER (WHERE t.team_id IS NOT NULL) AS teamlist
                from project_user_association pu
                LEFT JOIN user_info u ON u.user_id = pu.user_id
                LEFT JOIN teams_info t ON t.team_id = pu.team_id
                where pu.project_id = :project_id
            '''
            task_result = db.session.execute(
                    text(task_query), {"project_id":self.data['project_id'] }).fetchone()

            if task_result:
                return {
                    "status": True,
                    "message": "query successful",
                    "errorcode": 0,
                    "data": {
                        "users":task_result[0] if task_result[0] else [],
                        "teams":task_result[1] if task_result[1] else [],
                    }
                }

            return {
                    "status": False,
                    "message": "query failed",
                    "errorcode": 1,
                    "data": {}
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
