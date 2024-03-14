from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
import requests
from myapp.config import EMAIL_NOTIFY

class ProjectCreate:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewProj(self):
        try:
            ids = generate_uniqueId(type=['project'])
            ordered = [generate_uniqueId(type=['task_type'], delay=0.4)['task_type'] for i in range(3)]
            user_query = f'''
                insert into projects_info (project_id, department_id, organization_id, user_id, name, description, avatar, status, tools, links, task_order)
                values(:proj_id, :dept_id, :org_id, :user_id, :name, :description, :avatar, :status, :tools, :links, :tasks);
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
                        "tasks":ordered,
                    })
                session.commit()
            

            for items, item_id in zip(ordered, ['To Do', 'In Progress', 'Done']):
                tasktype_query = f'''
                    insert into task_types (type_id, project_id, department_id, name, created_by)
                    values(:type_id, :proj_id, :dept_id,  :name, :user_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(tasktype_query),
                        {
                            "type_id":items,
                            "proj_id":ids.get('project'),
                            "dept_id":self.data['dept_id'],
                            "name":item_id, 
                            "user_id": self.data['user_id'],
                        })
                    session.commit()

            for user in self.data['users']:
                ids_dept = generate_uniqueId(type=['project_user'], delay=0.2)
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

            res = requests.post(
                    EMAIL_NOTIFY.API+'/send-project-mail', 
                    json={"user_list":self.data['users'], "project_id":ids.get('project')},  
                    headers={'Content-Type':'application/json'})

            for team in self.data['teams']:
                ids_dept = generate_uniqueId(type=['project_user'], delay=0.2)
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
