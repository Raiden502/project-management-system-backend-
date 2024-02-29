from sqlalchemy import text
from myapp.db import db

class UserEditDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def update_details(self):
        try:
            user_query = f'''
                UPDATE user_info
                SET user_name = :name, email_addrs = :email, mobile_num =:phone, address=:address, role =:role, avatar=:avatar
                WHERE user_id= :user_id;
            '''    
            with db.session() as session:
                session.execute(
                    text(user_query), 
                    {
                        "name": self.data["name"],
                        "email":self.data['email'],
                        "phone":self.data['phone'],
                        "address":self.data['address'],
                        "role":self.data['role'],
                        "avatar":self.data['avatar'],
                        "user_id":self.data["user_id"]
                    })
                session.commit()
                return {
                    "status": True,
                    "message": "query successful",
                    "errorcode": 0,
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                }