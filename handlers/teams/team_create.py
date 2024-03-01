from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class TeamCreate:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewTeam(self):
        try:
            ids = generate_uniqueId(type=['team'])
            user_query = f'''
                insert into teams_info (team_id, department_id, organization_id, created_by, name, description, avatar)
                values(:team_id, :dept_id, :org_id, :user_id, :name, :description, :avatar);
            '''
            with db.session() as session:
                session.execute(
                    text(user_query),
                    {
                        "team_id":ids.get('team'),
                        "dept_id":self.data['dept_id'],
                        "org_id": self.data['org_id'],
                        "user_id": self.data['user_id'],
                        "name":self.data["name"], 
                        "description":self.data['description'],
                        "avatar":self.data["avatar"],
                    })
                session.commit()

            for user in self.data['users']:
                ids_dept = generate_uniqueId(type=['team_user'])
                dept_user_ads_query = f'''
                    insert into team_user_associaton (relation_id, team_id, user_id )
                    values(:rel_id, :team_id, :user_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "team_id": ids.get('team'),
                            "user_id": user,
                            "rel_id":ids_dept.get('team_user'),
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
