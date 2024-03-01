from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class UserTeamList:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_list(self):
        try:
            print(self.data['dept_id'])
            user_query = f''' 
                select u.user_id as id, u.user_name as name, u.email_addrs as email, u.avatar from user_info u
                join dept_user_associaton d on u.user_id = d.user_id
                where d.department_id = :dept_id
            '''  
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"dept_id":self.data['dept_id']})
                
                data =  dictfetchall(result)

                return {
                    "status": True,
                    "message": "query successful",
                    "errorcode": 0,
                    "data": data
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": {}
                }
