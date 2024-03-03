from sqlalchemy import text
from myapp.db import db


class GroupEditDetails:
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
                    array_agg(pu.user_id) FILTER (WHERE pu.user_id IS NOT NULL) AS userlist
                FROM group_info p
                LEFT JOIN user_group_associaton pu ON p.group_id = pu.group_id
                WHERE p.group_id = :group_id
                GROUP BY p.name, p.description, p.avatar
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"group_id":self.data['group_id'] })
                
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
                            "assignee":data[3] or [],
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
