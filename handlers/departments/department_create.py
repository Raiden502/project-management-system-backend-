from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
from utils.jwt_token import generate_token
from utils.generate_rand_pass import generate_password

class CreateDept:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewDept(self):
        try:
            ids = generate_uniqueId(type=['department'])
            user_query = f'''
                insert into department_info (department_id, organization_id, user_id, name, description, avatar)
                values(:department_id, :org_id, :user_id, :name, :description, :avatar);
            '''
            with db.session() as session:
                session.execute(
                    text(user_query),
                    {
                        "department_id":ids.get('department'),
                        "org_id": self.data['org_id'],
                        "user_id":self.data['user_id'],
                        "name":self.data["deptname"], 
                        "description":self.data['deptdesc'],
                        "avatar":self.data["avatar"],
                    })
                session.commit()

            for user in self.data['users']:
                ids_dept = generate_uniqueId(type=['department_user'])
                dept_user_ads_query = f'''
                    insert into dept_user_associaton (relation_id, user_id, department_id )
                    values(:rel_id, :user_id, :dept_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "dept_id": ids.get('department'),
                            "user_id": user,
                            "rel_id":ids_dept.get('department_user'),
                        })
                    session.commit()

            for team in self.data['teams']:
                ids_dept = generate_uniqueId(type=['department_user'])
                dept_user_ads_query = f'''
                    insert into dept_user_associaton (relation_id, team_id, department_id )
                    values(:rel_id, :team_id, :dept_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "dept_id": ids.get('department'),
                            "team_id": team,
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
