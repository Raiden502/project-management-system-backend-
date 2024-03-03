from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class UserChats:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_details_list(self):
        try:
            if(self.data['type'] == "group"):
                query = f'''
                    SELECT 
                        m.message, CASE when u.user_id =:sender_id THEN 'you' ELSE u.user_name END as username,
                        u.avatar,  m.created_at AS datetime, m.group_id AS receiverid, m.sender_id AS senderid from messages m
                    join
                    user_info u
                    on u.user_id = m.sender_id
                    WHERE
                    m.group_id = :receiver_id and m.organization_id = :org_id
                '''
            else:
                query = f'''
						SELECT message, created_at AS datetime, reciever_id AS receiverid, sender_id AS senderid from messages
						WHERE
						((sender_id = :sender_id AND reciever_id = :receiver_id) OR (reciever_id = :sender_id AND sender_id = :receiver_id))
                        and organization_id = :org_id
					'''

            data =  dictfetchall(
                    db.session.execute(
                    text(query), {"sender_id":self.data['sender_id'], "receiver_id":self.data['receiver_id'], "org_id":self.data['org_id']}))
            
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