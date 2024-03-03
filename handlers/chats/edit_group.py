from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId

class EditGroup:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def editGroup(self):
        try:
            group_id = self.data['group_id']

            update_query = f'''
                UPDATE group_info
                SET name = :name, description = :desc, avatar = :avatar
                WHERE group_id = :group_id
            '''
            with db.session() as session:
                session.execute(text(update_query), {
                    "group_id": group_id,
                    "name": self.data["name"],
                    "desc": self.data['desc'],
                    "avatar": self.data["avatar"],
                })
                session.commit()

            # Get existing user and team associations
            list_query = f'''
                SELECT
                    array_agg(user_id) FILTER (WHERE user_id IS NOT NULL) AS userlist
                FROM user_group_associaton
                WHERE group_id = :group_id
            '''
            result = db.session.execute(text(list_query), {"group_id": group_id}).fetchone()
            existing_users = result[0] or []

            # Update user associations
            users_to_add = [user for user in self.data['assignee'] if user not in existing_users]
            users_to_remove = [user for user in existing_users if user not in self.data['assignee']]

            for user in users_to_add:
                relation_id = generate_uniqueId(type=['group_user'])
                insert_query = f'''
                    INSERT INTO user_group_associaton (relation_id, user_id, group_id)
                    VALUES (:rel_id, :user_id, :group_id)
                '''
            
                db.session.execute(text(insert_query), {
                        "group_id": group_id,
                        "user_id": user,
                        "rel_id": relation_id.get('group_user'),
                    })
                db.session.commit()

            for user in users_to_remove:
                delete_query = f'''
                    DELETE FROM user_group_associaton
                    WHERE user_id = :user_id AND group_id = :group_id
                '''
                
                db.session.execute(text(delete_query), {
                        "group_id": group_id,
                        "user_id": user,
                    })
                db.session.commit()

            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
