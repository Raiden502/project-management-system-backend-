from sqlalchemy import text
from myapp.db import db


class Authenticate:
    def __init__(self, request):
        self.request = request

    def validate_token(self):
        try:
            login_query = f'''
                select 
                    user_id, organization_id, user_name, email_addrs,
                    mobile_num, verified, avatar, role
                from user_info where user_id =:user_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(login_query), {"user_id":self.request[0]})
                
                data = result.fetchone()

                if data:
                    return {
                        "status": True,
                        "message": "login successful",
                        "errorcode": 0,
                        "data": {
                            "user_id":data[0],
                            "org_id":data[1],
                            "user_name":data[2],
                            "email_address":data[3],
                            "mobile_num":data[4],
                            "verified": data[5],
                            "avatar":data[6],
                            "role":data[7]
                        }
                    }
                return {
                    "status": False,
                    "message": "login unsuccessful",
                    "errorcode": 1,
                    "data": {}
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "login unsuccessful",
                    "errorcode": 2,
                    "data": {}
                }
