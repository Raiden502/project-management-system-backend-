from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
import requests
from myapp.config import EMAIL_NOTIFY

class EditDept:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def editNewDept(self):
        try:
            department_id = self.data['department_id']

            update_query = f'''
                UPDATE department_info
                SET name = :name, description = :description, avatar = :avatar
                WHERE department_id = :department_id
            '''
            with db.session() as session:
                session.execute(text(update_query), {
                    "department_id": department_id,
                    "name": self.data["deptname"],
                    "description": self.data['deptdesc'],
                    "avatar": self.data["avatar"],
                })
                session.commit()

            # Get existing user and team associations
            list_query = f'''
                SELECT
                    array_agg(user_id) FILTER (WHERE user_id IS NOT NULL) AS userlist,
                    array_agg(team_id) FILTER (WHERE team_id IS NOT NULL) AS teamlist
                FROM dept_user_associaton
                WHERE department_id = :department_id
            '''
            result = db.session.execute(text(list_query), {"department_id": department_id}).fetchone()
            existing_users = result[0] or []
            existing_teams = result[1] or  []

            # Update user associations
            users_to_add = [user for user in self.data['users'] if user not in existing_users]
            users_to_remove = [user for user in existing_users if user not in self.data['users']]

            for user in users_to_add:
                relation_id = generate_uniqueId(type=['department_user'])
                insert_query = f'''
                    INSERT INTO dept_user_associaton (relation_id, user_id, department_id)
                    VALUES (:rel_id, :user_id, :dept_id)
                '''
            
                db.session.execute(text(insert_query), {
                        "dept_id": department_id,
                        "user_id": user,
                        "rel_id": relation_id.get('department_user'),
                    })
                db.session.commit()

            res = requests.post(EMAIL_NOTIFY.API+'/send-dept-mail', {"user_list":users_to_add})
            

            for user in users_to_remove:
                delete_query = f'''

                    DELETE FROM task_user_association
                    USING tasks t
                    WHERE t.task_id = task_user_association.task_id
                    AND t.department_id = :dept_id
                    AND task_user_association.user_id = :user_id;

                    DELETE FROM team_user_associaton
                    USING teams_info t
                    WHERE t.team_id = team_user_associaton.team_id
                    AND t.department_id = :dept_id
                    AND team_user_associaton.user_id = :user_id;

                    DELETE FROM project_user_association
                    WHERE user_id = :user_id AND department_id = :dept_id;

                    DELETE FROM dept_user_associaton
                    WHERE user_id = :user_id AND department_id = :dept_id;
                '''
                
                db.session.execute(text(delete_query), {
                        "dept_id": department_id,
                        "user_id": user,
                    })
                db.session.commit()

            # Update team associations
            teams_to_add = [team for team in self.data['teams'] if team not in existing_teams]
            teams_to_remove = [team for team in existing_teams if team not in self.data['teams']]

            for team in teams_to_add:
                relation_id = generate_uniqueId(type=['department_user'])
                insert_query = f'''
                    INSERT INTO dept_user_associaton (relation_id, team_id, department_id)
                    VALUES (:rel_id, :team_id, :dept_id)
                '''
                db.session.execute(text(insert_query), {
                        "dept_id": department_id,
                        "team_id": team,
                        "rel_id": relation_id.get('department_user'),
                    })
                db.session.commit()

            for team in teams_to_remove:
                delete_query = f'''
                    DELETE FROM task_user_association
                    USING tasks t
                    WHERE t.task_id = task_user_association.task_id
                    AND t.department_id = :dept_id
                    AND task_user_association.team_id = :team_id;

                    DELETE FROM project_user_association
                    WHERE team_id = :team_id AND department_id = :dept_id;

                    DELETE FROM dept_user_associaton
                    WHERE team_id = :team_id AND department_id = :dept_id;
                '''
                with db.session() as session:
                    session.execute(text(delete_query), {
                        "dept_id": department_id,
                        "team_id": team,
                    })
                    session.commit()

            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
