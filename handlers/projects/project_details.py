from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class ProjectDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_proj_details(self):
        try:
            proj_query = f''' 
                SELECT
                    p.project_id,
                    o.name,
                    p.name,
                    p.description,
                    p.created_date,
                    p.avatar,
                    p.status,
                    p.links,
                    p.tools,
                    p.task_count,
                    p.teams_count,
                    p.users_count,
                    array_agg(json_build_object('user_id', u.user_id, 'name', u.user_name, 'avatarUrl', u.avatar, 'role', u.role)) FILTER (WHERE u.user_id IS NOT NULL) AS userlist,
                    array_agg(json_build_object('team_id', t.team_id, 'name', t.name, 'avatarUrl', t.avatar, 'desc', t.description)) FILTER (WHERE t.team_id IS NOT NULL) AS teamlist,
                    de.name
                FROM projects_info p
                LEFT JOIN project_user_association pu ON p.project_id = pu.project_id
                LEFT JOIN user_info u ON u.user_id = pu.user_id
                LEFT JOIN teams_info t ON t.team_id = pu.team_id
                LEFT JOIN department_info de on de.department_id = p.department_id
                LEFT JOIN organization o on o.organization_id = de.organization_id
                WHERE p.department_id = :dept_id and p.project_id = :proj_id
                GROUP BY p.project_id, o.name, p.name, p.description, p.created_date, p.avatar, p.status, p.links, p.tools, p.task_count, p.teams_count, p.users_count, de.name
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"dept_id":self.data['dept_id'],"proj_id":self.data['proj_id'] })
                
                data =  result.fetchone()
                if data:
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": {
                            "project_id":data[0],
                            "organization_id":data[1],
                            "title":data[2],
                            "description":data[3],
                            "datePosted":data[4],
                            "avatar":data[5],
                            "status":data[6],
                            "links":data[7],
                            "tools":data[8],
                            "task_count":data[9],
                            "teams_count":data[10],
                            "users_count":data[11],
                            "contacts":data[12] or [],
                            "teams":data[13] or [],
                            "department":data[14]
                        }
                    }
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": {}
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": {}
                }
