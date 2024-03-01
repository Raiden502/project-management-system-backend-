from sqlalchemy import text
from myapp.db import db


class ProjectEditDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_proj_details(self):
        try:
            proj_query = f''' 
                SELECT
                    p.name,
                    p.description,
                    p.avatar,
                    p.status,
                    p.links,
                    p.tools,
                    array_agg(u.user_id) FILTER (WHERE u.user_id IS NOT NULL) AS userlist,
                    array_agg(t.team_id) FILTER (WHERE t.team_id IS NOT NULL) AS teamlist
                FROM projects_info p
                LEFT JOIN project_user_association pu ON p.project_id = pu.project_id
                LEFT JOIN user_info u ON u.user_id = pu.user_id
                LEFT JOIN teams_info t ON t.team_id = pu.team_id 
                WHERE p.project_id = :proj_id
                GROUP BY p.name, p.description, p.avatar, p.status, p.links, p.tools
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"proj_id":self.data['proj_id'] })
                
                data =  result.fetchone()
                if data:
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "name":data[0],
                            "desc":data[1],
                            "avatar":data[2],
                            "status":data[3],
                            "links":data[4],
                            "tools":data[5],
                            "users":data[6] or [],
                            "teams":data[7] or [],
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
