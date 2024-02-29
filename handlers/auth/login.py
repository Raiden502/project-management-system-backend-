from sqlalchemy import text
from myapp.db import db
from utils.jwt_token import generate_token


class Login:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def getuser(self):
        try:
            login_query = f'''
                select 
                    user_id, organization_id, user_name, email_addrs,
                    mobile_num, verified, avatar, role
                from user_info where user_password = :password and email_addrs = :email
            '''    
            with db.session() as session:
                result = session.execute(
                    text(login_query),
                    {
                        "password":self.data["password"],
                        "email":self.data["email"],
                    })
                
                data = result.fetchone()

                if data:
                    return {
                        "status": True,
                        "message": "login successful",
                        "errorcode": 0,
                        "data": {
                            'token': generate_token({"user_id":data[0]}),
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
