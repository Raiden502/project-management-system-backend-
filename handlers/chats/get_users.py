from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class UserDetails:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_details_list(self):
        try:
            user_query = f'''
                select 
                    g.group_id as id, g.name, False as onlinestatus, 'group' as type,
                    (
                    SELECT message FROM messages m WHERE m.group_id = group_id
                    ORDER BY m.created_at DESC
                    LIMIT 1
                    ) AS lastmsg,
                    avatar 
                from group_info g left join user_group_associaton ug on g.group_id = ug.group_id where g.organization_id = :org_id and ug.user_id = :user_id
                union
                select 
                    user_id as id, user_name as name, active_status as onlinestatus, 'normal' AS type,
                    (
                    SELECT message FROM messages m
                    WHERE 
                        (m.sender_id =:user_id and m.reciever_id = user_id) 
                        or (m.reciever_id =:user_id and m.sender_id = user_id)
                    ORDER BY m.created_at DESC
                    LIMIT 1
                    ) AS lastmsg,
                    avatar 
                from user_info where organization_id = :org_id and user_id!=:user_id;
            '''    
            with db.session() as session:
                result = session.execute(
                    text(user_query), {"org_id":self.data['org_id'], "user_id":self.data['user_id']})
                
                data =  dictfetchall(result)
                if len(data):
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": data
                    }
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": []
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": []
                }