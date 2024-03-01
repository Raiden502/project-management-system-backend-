from sqlalchemy import text
from myapp.db import db

class TeamDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_team_details(self):
        try:
            proj_query = f''' 
                SELECT
                    p.team_id,
                    o.name,
                    de.name,
                    p.name,
                    p.description,
                    p.created_at,
                    p.avatar,
                    p.user_count,
                    array_agg(json_build_object('user_id', u.user_id, 'name', u.user_name, 'avatarUrl', u.avatar, 'role', u.role)) FILTER (WHERE u.user_id IS NOT NULL) AS userlist
                FROM teams_info p
                LEFT JOIN team_user_associaton pu ON p.team_id = pu.team_id
                LEFT JOIN user_info u ON u.user_id = pu.user_id
                LEFT JOIN department_info de on de.department_id = p.department_id
                LEFT JOIN organization o on o.organization_id = de.organization_id
                WHERE p.department_id = :dept_id and p.team_id = :team_id
                GROUP BY p.team_id, o.name, p.name, p.description, p.created_at, p.avatar, p.user_count, de.name
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"dept_id":self.data['dept_id'],"team_id":self.data['team_id'] })
                
                data =  result.fetchone()
                if data:
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "team_id":data[0],
                            "organization":data[1],
                            "department":data[2],
                            "title":data[3],
                            "description":data[4],
                            "datePosted":data[5],
                            "avatar":data[6],
                            "users_count":data[7],
                            "contacts":data[8] or [],
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
