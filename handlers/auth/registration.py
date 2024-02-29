from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
from utils.jwt_token import generate_token

class Registration:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewUser(self):
        try:
            ids = generate_uniqueId(type=['user', 'organization', 'department', 'department_user'])
            print(ids)
            org_query = f'''
                insert into organization (organization_id, name, description)
                values(:org_id, :org_name, :org_desc);

                insert into user_info (user_id, organization_id, user_name, user_password, email_addrs, role)
                values(:user_id, :org_id, :username, :password, :email, :role);

                insert into department_info (department_id, organization_id, user_id, name, description)
                values(:dept_id, :org_id, :user_id, :dept_name, :dept_desc);

                insert into dept_user_associaton (relation_id, user_id, department_id )
                values(:rel_id, :user_id, :dept_id);
            '''    
            with db.session() as session:
                session.execute(
                    text(org_query),
                    {
                        "org_id":ids.get('organization'),
                        "user_id":ids.get('user'),
                        "dept_id":ids.get('department'),
                        "rel_id":ids.get('department_user'),
                        "org_name":self.data["org_name"],
                        "org_desc":self.data["org_desc"],
                        "username":self.data["username"], 
                        "password":self.data["password"],
                        "email":self.data["email"],
                        "role":"super_admin",
                        "dept_name":self.data["dept_name"],
                        "dept_desc":self.data["dept_desc"]
                    })
                session.commit()
            

            return {
                "status": True,
                "message": "registered successful",
                "errorcode": 0,
                "data": {
                    'token': generate_token({"user_id":ids.get('user')}),
                    "org_id":ids.get('organization'),
                    "user_id":ids.get('user'),
                    "user_name":self.data["username"],
                    "email_address":self.data["email"],
                    "mobile_num":"",
                    "verified": True,
                    "avatar":"",
                    "role": "super_admin"
                }
            }
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed to register", "errorcode": 2, "data": {}}
