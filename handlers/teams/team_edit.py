from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class EditTeams:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def editNewTeam(self):
        try:
            team_id = self.data['team_id']

            update_query = f'''
                UPDATE teams_info
                SET name = :name, description = :description, avatar = :avatar
                WHERE team_id = :team_id
            '''
            with db.session() as session:
                session.execute(text(update_query), {
                    "team_id": team_id,
                    "name": self.data["name"],
                    "description": self.data['description'],
                    "avatar": self.data["avatar"],
                })
                session.commit()

            # Get existing user and team associations
            list_query = f'''
                SELECT
                    array_agg(user_id) FILTER (WHERE user_id IS NOT NULL) AS userlist
                FROM team_user_associaton
                WHERE team_id = :team_id
            '''
            result = db.session.execute(text(list_query), {"team_id": team_id}).fetchone()
            existing_users = result[0] or []

            # Update user associations
            users_to_add = [user for user in self.data['users'] if user not in existing_users]
            users_to_remove = [user for user in existing_users if user not in self.data['users']]

            for user in users_to_add:
                relation_id = generate_uniqueId(type=['team_user'])
                insert_query = f'''
                    INSERT INTO team_user_associaton (relation_id, user_id, team_id)
                    VALUES (:rel_id, :user_id, :team_id)
                '''
            
                db.session.execute(text(insert_query), {
                        "team_id": team_id,
                        "user_id": user,
                        "rel_id": relation_id.get('team_user'),
                    })
                db.session.commit()

            for user in users_to_remove:
                delete_query = f'''
                    DELETE FROM team_user_associaton
                    WHERE user_id = :user_id AND team_id = :team_id
                '''
                
                db.session.execute(text(delete_query), {
                        "team_id": team_id,
                        "user_id": user,
                    })
                db.session.commit()

            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
