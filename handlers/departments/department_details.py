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
                    o.name
                FROM department_info di
                LEFT JOIN organization o on o.organization_id = di.organization_id
                WHERE di.department_id = :dept_id;
            '''

            user_list_query = f'''
                SELECT
                    COALESCE(json_agg(json_build_object('user_id', u.user_id, 'name', u.user_name, 'avatarUrl', u.avatar, 'role', u.role)), '[]'::json)
                FROM user_info u left join dept_user_associaton d on u.user_id = d.user_id 
                WHERE d.department_id = :dept_id;
                '''
            team_list_query = f'''
                SELECT
                    COALESCE(json_agg(json_build_object('team_id', t.team_id, 'name', t.name, 'avatarUrl', t.avatar, 'desc', t.description)), '[]'::json)
                FROM teams_info t left join dept_user_associaton d on t.team_id = d.team_id
                WHERE  d.department_id = :dept_id;
            '''

            data = db.session.execute(
                text(dept_query), {"dept_id":self.data['dept_id']}).fetchone()

            if data:
                users = db.session.execute(text(user_list_query), {"dept_id":self.data['dept_id']}).fetchone()
                teams = db.session.execute(text(team_list_query), {"dept_id":self.data['dept_id']}).fetchone()
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
                        "organization":data[9],
                        "contacts": users[0],
                        "teams": teams[0]
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
