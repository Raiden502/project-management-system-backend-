from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class DepartmentEditDetails:
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
                    di.avatar
                FROM department_info di
                WHERE di.department_id = :dept_id
            '''    
            data = db.session.execute(
                    text(dept_query), {"dept_id":self.data['dept_id']}).fetchone()

            user_list_query = f'''
                SELECT
                    array_agg(u.user_id) FILTER (WHERE u.user_id IS NOT NULL) AS userlist
                FROM user_info u left join dept_user_associaton d on u.user_id = d.user_id 
                WHERE d.department_id = :dept_id;
                '''
            team_list_query = f'''
                SELECT
                    array_agg(d.team_id) FILTER (WHERE d.team_id IS NOT NULL) AS teamlist
                FROM teams_info t left join dept_user_associaton d on t.team_id = d.team_id
                WHERE  d.department_id = :dept_id;
            '''

            if data:
                users = db.session.execute(text(user_list_query), {"dept_id":self.data['dept_id']}).fetchone()
                teams = db.session.execute(text(team_list_query), {"dept_id":self.data['dept_id']}).fetchone()
                return {
                    "status": True,
                    "message": "query successful",
                    "errorcode": 0,
                    "data": {
                        "department_id":data[0],
                        "deptname":data[1],
                        "deptdesc":data[2],
                        "avatar":data[3],
                        "users":users[0] or [],
                        "teams":teams[0] or []
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
