from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class OrgUserDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_details_list(self):
        try:
            user_query = f'''
                select user_id, user_name as name, avatar, email_addrs 
                from user_info where organization_id = :org_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"org_id":self.data['org_id']})
                data =  dictfetchall(result)
                if len(data):
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": data
                    }
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": []
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": []
                }