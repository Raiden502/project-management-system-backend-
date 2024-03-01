from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class DepartmentDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_dept_details(self):
        try:
            dept_query = f''' 
                SELECT
                    di.department_id,
                    di.name,
                    di.description,
                    di.created_date,
                    di.avatar,
                    di.project_count,
                    di.task_count,
                    di.teams_count,
                    di.users_count,
                    array_agg(json_build_object('user_id', u.user_id, 'name', u.user_name, 'avatarUrl', u.avatar, 'role', u.role)) FILTER (WHERE u.user_id IS NOT NULL) AS userlist,
                    o.name,
                    array_agg(json_build_object('team_id', t.team_id, 'name', t.name, 'avatarUrl', t.avatar, 'desc', t.description)) FILTER (WHERE t.team_id IS NOT NULL) AS teamlist
                FROM user_info u
                LEFT JOIN dept_user_associaton d ON d.user_id = u.user_id
                LEFT JOIN department_info di ON d.department_id = di.department_id
                LEFT JOIN teams_info t ON t.team_id = d.team_id
                LEFT JOIN organization o on o.organization_id = di.organization_id
                WHERE di.department_id = :dept_id
                GROUP BY di.department_id, di.name, di.description, di.created_date, di.avatar, 
                di.project_count, di.task_count, di.teams_count,di.users_count, o.name
            '''    
            with db.session() as session:
                result = session.execute(
                    text(dept_query), {"dept_id":self.data['dept_id']})
                
                data =  result.fetchone()
                if data:
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "department_id":data[0],
                            "title":data[1],
                            "department":data[1],
                            "description":data[2],
                            "datePosted":data[3],
                            "avatar":data[4],
                            "project_count":data[5],
                            "task_count":data[6],
                            "teams_count":data[7],
                            "users_count":data[8],
                            "contacts":data[9] or [],
                            "organization":data[10],
                            "teams":data[11] or []
                        }
                    }
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": {}
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": {}
                }
