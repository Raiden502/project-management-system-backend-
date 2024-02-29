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
                    di.avatar,
                    array_agg(u.user_id) FILTER (WHERE u.user_id IS NOT NULL) AS userlist,
                    array_agg(d.team_id) FILTER (WHERE d.team_id IS NOT NULL) AS teamlist
                FROM user_info u
                LEFT JOIN dept_user_associaton d ON d.user_id = u.user_id
                LEFT JOIN department_info di ON d.department_id = di.department_id
                WHERE di.department_id = :dept_id
                GROUP BY di.department_id, di.name, di.description, di.avatar
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
                            "deptname":data[1],
                            "deptdesc":data[2],
                            "avatar":data[3],
                            "users":data[4] or [],
                            "teams":data[5] or []
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
