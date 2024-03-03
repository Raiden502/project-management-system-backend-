from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class CreateGroup:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def addNewUser(self):
        try:
            ids = generate_uniqueId(type=['group'])
            user_query = f'''
                insert into group_info(group_id, organization_id, created_by, name, description,  avatar)
                values(:group_id, :org_id, :user_id, :name, :desc, :avatar);
            '''
            with db.session() as session:
                session.execute(
                    text(user_query),
                    {
                        "group_id":ids.get('group'),
                        "org_id": self.data['org_id'],
                        "user_id":self.data['user_id'],
                        "name":self.data["name"], 
                        "desc":self.data["desc"],
                        "avatar":self.data["avatar"],
                    })
                session.commit()

            for user in self.data['assignee']:
                ids_dept = generate_uniqueId(type=['group_user'])
                dept_user_ads_query = f'''
                    insert into user_group_associaton (relation_id, user_id, group_id )
                    values(:rel_id, :user_id, :group_id);
                '''
                with db.session() as session:
                    session.execute(
                        text(dept_user_ads_query),
                        {
                            "group_id": ids.get('group'),
                            "user_id": user,
                            "rel_id":ids_dept.get('group_user'),
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
