from sqlalchemy import text
from myapp.db import db
from utils.generate_uniqueid import generate_uniqueId
from utils.email_notify import notify_mail

class EditTask:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def editNewTask(self):
        try:
            project_id = self.data['project_id']
            task_id = self.data['id']
            type_id =self.data['column']

            update_query = f'''
                UPDATE tasks
                SET name = :name, description = :description, labels = :labels, reporter = :reporter, priority = :priority, start_date = :start_date, due_date = :due_date
                WHERE project_id =:project_id and task_id =:task_id and type_id =:type_id
            '''
            with db.session() as session:
                session.execute(text(update_query), {
                    "project_id": project_id,
                    "task_id":task_id,
                    "type_id":type_id,
                    "name": self.data["name"],
                    "description": self.data['description'],
                    "labels": self.data["labels"],
                    "reporter": self.data["reporter"],
                    "priority": self.data["priority"],
                    "start_date":self.data['start_date'],
                    "due_date": self.data["due_date"],
                })
                session.commit()

            # Get existing user and team associations
            list_query = f'''
                SELECT
                    array_agg(user_id) FILTER (WHERE user_id IS NOT NULL) AS userlist,
                    array_agg(team_id) FILTER (WHERE team_id IS NOT NULL) AS teamlist
                FROM task_user_association
                WHERE project_id = :project_id and task_id =:task_id
            '''
            result = db.session.execute(text(list_query), {"project_id": project_id, "task_id":task_id}).fetchone()
            existing_users = result[0] or []
            existing_teams = result[1] or  []


            # Update user associations
            users_to_add = [user for user in self.data['users'] if user not in existing_users]
            users_to_remove = [user for user in existing_users if user not in self.data['users']]

            for user in users_to_add:
                relation_id = generate_uniqueId(type=['task_users'])
                insert_query = f'''
                    INSERT INTO task_user_association (relation_id, user_id, project_id, task_id)
                    VALUES (:rel_id, :user_id, :project_id, :task_id)
                '''
            
                db.session.execute(text(insert_query), {
                        "project_id": project_id,
                        "user_id": user,
                        "rel_id": relation_id.get('task_users'),
                        "task_id": task_id
                    })
                db.session.commit()
            for user in users_to_remove:
                delete_query = f'''
                    DELETE FROM task_user_association
                    WHERE user_id = :user_id AND project_id = :project_id and task_id = :task_id
                '''
                
                db.session.execute(text(delete_query), {
                        "project_id": project_id,
                        "task_id":task_id,
                        "user_id": user,
                    })
                db.session.commit()

            # Update team associations
            teams_to_add = [team for team in self.data['teams'] if team not in existing_teams]
            teams_to_remove = [team for team in existing_teams if team not in self.data['teams']]

            for team in teams_to_add:
                relation_id = generate_uniqueId(type=['task_users'])
                insert_query = f'''
                    INSERT INTO task_user_association (relation_id, team_id, project_id, task_id)
                    VALUES (:rel_id, :team_id, :project_id, :task_id)
                '''
                db.session.execute(text(insert_query), {
                        "project_id": project_id,
                        "team_id": team,
                        "rel_id": relation_id.get('task_users'),
                        "task_id": task_id
                    })
                db.session.commit()

            for team in teams_to_remove:
                delete_query = f'''
                    DELETE FROM task_user_association
                    WHERE team_id = :team_id AND project_id = :project_id and task_id = :task_id
                '''
                with db.session() as session:
                    session.execute(text(delete_query), {
                        "project_id": project_id,
                        "task_id":task_id,
                        "team_id": team,
                    })
                    session.commit()


            # attachments            
            list_query = f'''
                SELECT
                    array_agg(relation_id) FILTER (WHERE relation_id IS NOT NULL) AS id
                FROM task_files_associaton
                WHERE task_id =:task_id
            '''
            result = db.session.execute(text(list_query), {"task_id":task_id}).fetchone()
            existing_users = result[0] or []

            check_files = [it['id'] for it in self.data['attachments'] if it['id']!='']

            users_to_remove = [files for files in existing_users if files not in check_files]

            print(users_to_remove, existing_users, check_files)

            for item in users_to_remove:
                delete_query = f'''
                    DELETE FROM task_files_associaton
                    WHERE  relation_id =:rel_id and task_id = :task_id
                '''
                
                db.session.execute(text(delete_query), {
                        "rel_id": item,
                        "task_id":task_id,
                    })
                db.session.commit()

            for files in self.data['attachments']:
                if files['id']=='':
                    relation_id = generate_uniqueId(type=['task_file'])
                    insert_query = f'''
                        INSERT INTO task_files_associaton (relation_id, task_id, file_src)
                        VALUES (:rel_id, :task_id, :src)
                    '''
                    db.session.execute(text(insert_query), {
                            "src":files['file'],
                            "rel_id": relation_id.get('task_file'),
                            "task_id": task_id
                        })
                    db.session.commit()

            notify_mail('/send-task-mail',{"user_list":users_to_add, "project_id":project_id, "task_id":task_id})
            return {"status": True, "message": "registered successful", "errorcode": 0}
        except Exception as e:
            print(e)
            return {"status": False, "message": "failed", "errorcode":2}
