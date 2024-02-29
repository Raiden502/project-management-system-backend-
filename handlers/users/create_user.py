from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
from utils.jwt_token import generate_token
from utils.generate_rand_pass import generate_password

class CreateUser:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewUser(self):
        try:
            ids = generate_uniqueId(type=['user'])
            user_query = f'''
                insert into user_info (user_id, organization_id, user_name, user_password, email_addrs, role, address, mobile_num, avatar)
                values(:user_id, :org_id, :username, :password, :email, :role, :address, :phone, :avatar);
            '''
            with db.session() as session:
                session.execute(
                    text(user_query),
                    {
                        "org_id": self.data['org_id'],
                        "user_id":ids.get('user'),
                        "username":self.data["name"], 
                        "password":generate_password(),
                        "email":self.data["email"],
                        "address":self.data['address'],
                        "phone":self.data['phone'],
                        "role":self.data['role'],
                        "avatar":self.data["avatar"],
                    })
                session.commit()

            for dept in self.data['departments']:
                ids_dept = generate_uniqueId(type=['department_user'])
                dept_user_ads_query = f'''
                    insert into dept_user_associaton (relation_id, user_id, department_id )
                    values(:rel_id, :user_id, :dept_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "dept_id": dept,
                            "user_id":ids.get('user'),
                            "rel_id":ids_dept.get('department_user'),
                        })
                    session.commit()

            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2}
