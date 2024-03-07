from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class DeleteTeams:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def delete(self):
        try:
            team_id = self.data['team_id']
            dept_id = self.data['dept_id']

            delete_query = f'''

                DELETE FROM task_user_association
                USING teams_info t
                WHERE t.team_id = task_user_association.team_id
                AND t.department_id = :dept_id
                AND task_user_association.team_id = :team_id;

                DELETE FROM project_user_association
                WHERE team_id = :team_id AND department_id = :dept_id;

                DELETE FROM team_user_associaton
                USING teams_info t
                WHERE t.team_id = team_user_associaton.team_id
                AND t.department_id = :dept_id
                AND team_user_associaton.team_id = :team_id;

                DELETE FROM dept_user_associaton
                WHERE team_id = :team_id;

                DELETE FROM teams_info
                WHERE team_id = :team_id;
                
            '''
            db.session.execute(text(delete_query), {
                    "team_id": team_id,
                    "dept_id": dept_id,
                })
            db.session.commit()

            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
