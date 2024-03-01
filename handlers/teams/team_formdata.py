from sqlalchemy import text
from myapp.db import db


class TeamEditDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_form_details(self):
        try:
            proj_query = f''' 
                SELECT
                    p.name,
                    p.description,
                    p.avatar,
                    array_agg(u.user_id) FILTER (WHERE u.user_id IS NOT NULL) AS userlist
                FROM teams_info p
                LEFT JOIN team_user_associaton pu ON p.team_id = pu.team_id
                LEFT JOIN user_info u ON u.user_id = pu.user_id
                WHERE p.team_id = :team_id
                GROUP BY p.name, p.description, p.avatar
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"team_id":self.data['team_id'] })
                
                data =  result.fetchone()
                if data:
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "name":data[0],
                            "description":data[1],
                            "avatar":data[2],
                            "users":data[3] or [],
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
