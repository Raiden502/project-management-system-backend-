from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class UserDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_details_list(self):
        try:
            user_query = f'''
                select 
                    u.user_id, u.user_name, u.email_addrs, u.mobile_num, u.address, u.verified, role, avatar 
                    from user_info u join dept_user_associaton d
                on d.user_id = u.user_id 
                where d.department_id = :department_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"department_id":self.data['department_id']}) # {"user_id":self.request[0]}
                
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
    
    def get_details(self):
        try:
            user_query = f'''
                SELECT
                    u.user_id,
                    u.user_name,
                    u.email_addrs,
                    u.mobile_num,
                    u.address,
                    role,
                    avatar,
                    array_agg(d.department_id) AS deptlist
                FROM user_info u
                LEFT JOIN dept_user_associaton d ON d.user_id = u.user_id
                WHERE u.user_id = :user_id
                GROUP BY u.user_id, u.user_name, u.email_addrs, u.mobile_num, u.address, role, avatar;
            '''    
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"user_id":self.data['user_id']}) # {"user_id":self.request[0]}
                
                data = result.fetchone()
                print(data)
                if len(data):
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "user_id":data[0],
                            "name": data[1],
                            "email": data[2],
                            "phone": data[3],
                            "address": data[4],
                            "role": data[5],
                            "avatar": data[6],
                            "departments": data[7],
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
