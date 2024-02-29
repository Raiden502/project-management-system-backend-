from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class TeamUserDeptList:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_list(self):
        try:
            user_query = f''' 
                select user_id as id, user_name as name, email_addrs as email, avatar from user_info where organization_id = :org_id
            '''  
            team_query = f''' 
                select team_id as id, name as name, avatar from teams_info where organization_id = :org_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"org_id":self.data['org_id']})
                
                result2 = session.execute(
                    text(team_query), {"org_id":self.data['org_id']})
                
                data =  dictfetchall(result)
                data2 =  dictfetchall(result2)

                return {
                    "status": True,
                    "message": "query successful",
                    "errorcode": 0,
                    "data": {
                        "users":data,
                        "teams":data2,
                    }
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": {}
                }
