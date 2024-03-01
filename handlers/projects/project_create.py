from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class ProjectCreate:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewProj(self):
        try:
            ids = generate_uniqueId(type=['project'])
            user_query = f'''
                insert into projects_info (project_id, department_id, organization_id, user_id, name, description, avatar, status, tools, links)
                values(:proj_id, :dept_id, :org_id, :user_id, :name, :description, :avatar, :status, :tools, :links);
            '''
            with db.session() as session:
                session.execute(
                    text(user_query),
                    {
                        "proj_id":ids.get('project'),
                        "dept_id":self.data['dept_id'],
                        "org_id": self.data['org_id'],
                        "user_id": self.data['user_id'],
                        "name":self.data["name"], 
                        "description":self.data['desc'],
                        "avatar":self.data["avatar"],
                        "status":self.data['status'],
                        "tools": self.data['tools'],
                        "links": self.data['links'],
                    })
                session.commit()

            for user in self.data['users']:
                ids_dept = generate_uniqueId(type=['project_user'])
                dept_user_ads_query = f'''
                    insert into project_user_association (relation_id, project_id,  user_id, department_id )
                    values(:rel_id, :proj_id, :user_id, :dept_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "proj_id": ids.get('project'),
                            "dept_id": self.data['dept_id'],
                            "user_id": user,
                            "rel_id":ids_dept.get('project_user'),
                        })
                    session.commit()

            for team in self.data['teams']:
                ids_dept = generate_uniqueId(type=['project_user'])
                dept_user_ads_query = f'''
                    insert into project_user_association (relation_id, project_id, team_id, department_id )
                    values(:rel_id, :proj_id, :team_id, :dept_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "proj_id": ids.get('project'),
                            "dept_id": self.data['dept_id'],
                            "team_id": team,
                            "rel_id":ids_dept.get('project_user'),
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